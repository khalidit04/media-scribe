"""
Tests for media extraction logic using FFmpeg.
"""
from unittest.mock import patch
import pytest
from media_scribe.extractor import extract_audio
from media_scribe.exceptions import MediaExtractionError

@patch("media_scribe.extractor.ffmpeg")
def test_extract_audio_success(mock_ffmpeg, tmp_path):
    """Test successful audio extraction from a media file."""
    # Setup mock input file
    input_file = tmp_path / "test_video.mp4"
    input_file.write_text("dummy video content", encoding="utf-8")

    # Mock ffmpeg run
    mock_ffmpeg.run.return_value = None

    # Run extractor
    output_wav = extract_audio(str(input_file))

    # Assert
    assert output_wav == str(tmp_path / "test_video_extracted.wav")
    mock_ffmpeg.input.assert_called_once_with(str(input_file))
    mock_ffmpeg.output.assert_called_once()
    mock_ffmpeg.run.assert_called_once()

def test_extract_audio_file_not_found():
    """Test that a non-existent file raises MediaExtractionError."""
    with pytest.raises(MediaExtractionError) as exc_info:
        extract_audio("nonexistent_file.mp4")
    assert "Input file not found" in str(exc_info.value)
