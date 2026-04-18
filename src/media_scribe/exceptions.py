"""
Custom exception classes for MediaScribe.
"""

class MediaScribeError(Exception):
    """Base exception for all MediaScribe errors."""
    pass

class MediaExtractionError(MediaScribeError):
    """Raised when audio/video extraction via FFmpeg fails."""
    pass

class TranscriptionTimeoutError(MediaScribeError):
    """Raised when STT translation takes too long and times out."""
    pass

class LanguageNotSupportedError(MediaScribeError):
    """Raised when the specified or detected language is unsupported."""
    pass
