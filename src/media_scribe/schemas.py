"""
Pydantic schemas for MediaScribe output definitions.
"""
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class TranscriptSegment(BaseModel):
    start_time: float
    end_time: float
    text: str

class ContentSummary(BaseModel):
    gist: str
    key_points: List[str]

class MediaScribeResult(BaseModel):
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
