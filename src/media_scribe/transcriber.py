"""
Uses MLX-Whisper for high speed inference on Apple Silicon.
"""
import time
from typing import Dict, Any
import mlx_whisper
from media_scribe.logger import logger
from media_scribe.schemas import MediaScribeResult, TranscriptSegment
from media_scribe.utils import timeout

@timeout(600)
def transcribe_audio(file_path: str,
                    model_path: str = "mlx-community/whisper-small-mlx") -> MediaScribeResult:
    """
    Transcribes an audio file using MLX-Whisper and returns a typed MediaScribeResult.
    Using 'whisper-small-mlx' by default. 'whisper-large-v3-mlx' can be passed for accuracy.
    """
    start_time = time.time()
    logger.info("Starting transcription via MLX Whisper", file=file_path, model=model_path)

    try:
        # condition_on_previous_text=False prevents hallucinations loops
        result: Dict[str, Any] = mlx_whisper.transcribe(
            file_path,
            path_or_hf_repo=model_path,
            condition_on_previous_text=False
        )
    except Exception as e:
        logger.error("Transcription failed", error=str(e))
        raise

    process_time_ms = int((time.time() - start_time) * 1000)

    detected_language = result.get("language", "unknown")
    text = result.get("text", "")
    segments_raw = result.get("segments", [])

    # Calculate duration safely by checking last segment
    duration = 0.0
    if segments_raw:
        duration = segments_raw[-1].get("end", 0.0)

    segments = [
        TranscriptSegment(
            start_time=seg.get("start", 0.0),
            end_time=seg.get("end", 0.0),
            text=seg.get("text", "")
        )
        for seg in segments_raw
    ]

    logger.info("Transcription completed",
                duration_seconds=duration,
                detected_language=detected_language,
                process_time_ms=process_time_ms)

    return MediaScribeResult(
        file_id=file_path,
        original_format="wav",
        detected_language=detected_language,
        duration_seconds=duration,
        full_text=text,
        segments=segments,
        processing_time_ms=process_time_ms
    )
