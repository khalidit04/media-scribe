"""
Cross-platform transcriber supporting MLX-Whisper (macOS ARM) and OpenAI-Whisper (Unix/Other).
"""
import time
from typing import Dict, Any

try:
    import mlx_whisper as MLX_ENGINE
    HAS_MLX = True
    STANDARD_ENGINE = None
except ImportError:
    import whisper as STANDARD_ENGINE
    HAS_MLX = False
    MLX_ENGINE = None

from media_scribe.logger import logger
from media_scribe.schemas import MediaScribeResult, TranscriptSegment
from media_scribe.utils import timeout

@timeout(600)
def transcribe_audio(file_path: str, model_path: str = None) -> MediaScribeResult:
    """
    Transcribes an audio file using available engine (MLX-Whisper or OpenAI-Whisper).
    Returns a typed MediaScribeResult.
    """
    start_time = time.time()
    # Identify best default model if none provided
    if not model_path:
        model_path = "mlx-community/whisper-small-mlx" if HAS_MLX else "small"

    engine_name = "MLX-Whisper" if HAS_MLX else "OpenAI-Whisper"
    logger.info(f"Starting transcription via {engine_name}", file=file_path, model=model_path)

    try:
        if HAS_MLX:
            # Condition_on_previous_text=False prevents hallucinations loops
            result: Dict[str, Any] = MLX_ENGINE.transcribe(
                file_path,
                path_or_hf_repo=model_path,
                condition_on_previous_text=False
            )
        else:
            # Using standard OpenAI Whisper for Unix/Linux
            model = STANDARD_ENGINE.load_model(model_path)
            result: Dict[str, Any] = model.transcribe(
                file_path,
                condition_on_previous_text=False
            )
    except Exception as e:
        logger.error("Transcription failed", engine=engine_name, error=str(e))
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
                engine=engine_name,
                duration_seconds=round(duration, 2),
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
