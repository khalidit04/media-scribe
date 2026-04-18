"""
Audio cleaning utilities, applying noise reduction safely without blowing up memory.
"""
import os
import soundfile as sf
import noisereduce as nr
from media_scribe.logger import logger
from media_scribe.exceptions import MediaScribeError

def apply_noise_reduction(input_wav: str, chunk_duration_sec: int = 300) -> str:
    """
    Reads the input_wav chunk-by-chunk to prevent OOM errors, applies noisereduce, 
    and writes to a new intermediate file. Returns path to cleaned wav.
    """
    if not os.path.exists(input_wav):
        raise MediaScribeError(f"File not found for noise reduction: {input_wav}")

    base, ext = os.path.splitext(input_wav)
    output_wav = f"{base}_cleaned{ext}"

    logger.info("Starting chunk-by-chunk noise reduction",
                input_file=input_wav, chunk_duration=chunk_duration_sec)

    try:
        with sf.SoundFile(input_wav) as f_in:
            sr = f_in.samplerate
            channels = f_in.channels

            # chunk_duration_sec seconds * sample_rate = frames per chunk
            chunk_size = sr * chunk_duration_sec

            with sf.SoundFile(output_wav, 'w', samplerate=sr, channels=channels) as f_out:
                for block in f_in.blocks(blocksize=chunk_size):
                    # sf blocks are (frames, channels) or (frames,) for mono
                    # nr.reduce_noise expects (channels, frames) or (frames,)

                    cleaned_block = nr.reduce_noise(y=block.T, sr=sr)

                    # Write it back. If it was 1D, we just write it without .T
                    # block.T gives (channels, frames), we need (frames, channels) back
                    f_out.write(cleaned_block.T)

        logger.info("Noise reduction completed successfully", output_file=output_wav)
        return output_wav
    except Exception as e:
        logger.error("Failed to apply noise reduction", error=str(e), file=input_wav)
        raise MediaScribeError(f"Noise reduction failed: {str(e)}") from e
