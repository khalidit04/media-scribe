"""
Package initialization for MediaScribe.
"""
from media_scribe.core import process_media
from media_scribe.schemas import MediaScribeResult
from media_scribe.exceptions import MediaScribeError

__version__ = "0.1.0"
__all__ = ["process_media", "MediaScribeResult", "MediaScribeError"]
