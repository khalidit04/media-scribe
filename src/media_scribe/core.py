"""
Main entry module for MediaScribe.
"""
import os
from media_scribe.extractor import extract_audio
from media_scribe.transcriber import transcribe_audio
from media_scribe.schemas import MediaScribeResult
from media_scribe.logger import logger

def process_media(file_path: str, model_size: str = "mlx-community/whisper-tiny-mlx") -> MediaScribeResult:
    """
    End-to-end pipeline: Extracts audio from ANY media file and runs it through MLX Whisper.
    """
    logger.info("Starting MediaScribe processing pipeline", file=file_path)
    
    # 1. Extract and standardize audio
    wav_path = extract_audio(file_path)
    
    try:
        # 2. Transcribe
        result = transcribe_audio(wav_path, model_path=model_size)
    finally:
        # Clean up temporary extracted WAV if we generated one
        if wav_path != file_path and os.path.exists(wav_path):
            os.remove(wav_path)
            logger.info("Cleaned up temporary wav file", wav_path=wav_path)
            
    return result
