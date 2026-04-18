"""
Main entry module for MediaScribe.
"""
import os
from media_scribe.extractor import extract_audio
from media_scribe.cleaner import apply_noise_reduction
from media_scribe.transcriber import transcribe_audio
from media_scribe.schemas import MediaScribeResult
from media_scribe.plugins import BaseNLPProvider, OllamaProvider
from media_scribe.logger import logger

def process_media(file_path: str, model_size: str = "mlx-community/whisper-small-mlx",
                  clean_audio: bool = False, summarize: bool = False,
                  translation_lang: str = None,
                  nlp_provider: BaseNLPProvider = None) -> MediaScribeResult: # pylint: disable=too-many-arguments, too-many-positional-arguments
    """
    End-to-end pipeline: Extracts audio from ANY media file and runs it through MLX Whisper.
    """
    logger.info("Starting MediaScribe pipeline", file=file_path, clean_audio=clean_audio)

    # 1. Extract and standardize audio
    wav_path = extract_audio(file_path)
    cleaned_wav_path = None

    try:
        if clean_audio:
            cleaned_wav_path = apply_noise_reduction(wav_path)
            target_wav = cleaned_wav_path
        else:
            target_wav = wav_path

        # 2. Transcribe
        result = transcribe_audio(target_wav, model_path=model_size)

        # 3. Handle Extensions (Summarization & Translation)
        if summarize or translation_lang:
            # Use provided provider or default to Ollama
            provider = nlp_provider or OllamaProvider()

            if summarize:
                result.summary = provider.summarize(result.full_text)
            if translation_lang:
                result.target_translation = provider.translate(result.full_text, translation_lang)
    finally:
        # Clean up temporary extracted WAV if we generated one
        if wav_path != file_path and os.path.exists(wav_path):
            os.remove(wav_path)
            logger.info("Cleaned up temporary wav file", wav_path=wav_path)

        if cleaned_wav_path and os.path.exists(cleaned_wav_path):
            os.remove(cleaned_wav_path)
            logger.info("Cleaned up temporary denoised wav file", wav_path=cleaned_wav_path)

    return result

def export_to_json(result: MediaScribeResult, output_path: str) -> str:
    """
    Serializes securely typed JSON to the given path for future downstream parsing.
    Returns the path to the generated JSON file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.model_dump_json(indent=2))

    logger.info("JSON file exported", output_path=output_path)
    return output_path
