"""
Logic for extracting audio from video schemas and chunking large audio files.
"""
import os
import ffmpeg
from media_scribe.exceptions import MediaExtractionError
from media_scribe.logger import logger

def extract_audio(input_file: str, output_file: str = None, sample_rate: int = 16000) -> str:
    """
    Extracts audio from a given media file and converts it to standard 16kHz mono WAV.
    Required by Whisper models for optimal inference.
    """
    if not os.path.exists(input_file):
        logger.error("Input file not found", file=input_file)
        raise MediaExtractionError(f"Input file not found: {input_file}")

    if not output_file:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}_extracted.wav"

    logger.info("Extracting audio...", input_file=input_file, output_file=output_file)

    try:
        # We enforce 1 channel (mono) and standard whisper sample rate
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file, ac=1, ar=sample_rate, loglevel="error")
        ffmpeg.run(stream, overwrite_output=True)

        logger.info("Audio extracted successfully", output_file=output_file)
        return output_file
    except ffmpeg.Error as e:
        logger.error("FFmpeg extraction failed", error=str(e), input_file=input_file)
        raise MediaExtractionError(f"FFmpeg failed to extract from {input_file}") from e
