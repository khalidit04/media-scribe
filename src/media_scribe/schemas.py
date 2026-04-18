"""
Pydantic schemas for MediaScribe output definitions.
"""
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class TranscriptSegment(BaseModel):
    """Represents a segment of the transcription with timestamps."""
    start_time: float
    end_time: float
    text: str

class ContentSummary(BaseModel):
    """Represents a summary/gist of the media content."""
    gist: str
    key_points: List[str]

class MediaScribeResult(BaseModel):
    """The final structured result of the MediaScribe pipeline."""
    model_config = ConfigDict(strict=True)

    file_id: str
    original_format: str
    detected_language: str
    duration_seconds: float
    full_text: str
    segments: List[TranscriptSegment]
    summary: Optional[ContentSummary] = None
    target_translation: Optional[str] = None
    processing_time_ms: int
