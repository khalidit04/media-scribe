import pytest
from unittest.mock import patch
from media_scribe.transcriber import transcribe_audio
from media_scribe.schemas import MediaScribeResult

@patch("media_scribe.transcriber.mlx_whisper")
def test_transcribe_audio_success(mock_mlx_whisper, tmp_path):
    # Mock MLX Whisper output
    mock_mlx_whisper.transcribe.return_value = {
        "text": "Hello world.",
        "language": "en",
        "segments": [
            {"start": 0.0, "end": 1.5, "text": "Hello world."}
        ]
    }
    
    input_file = tmp_path / "test_audio.wav"
    input_file.write_text("dummy")
    
    result = transcribe_audio(str(input_file), model_path="tiny")
    
    assert isinstance(result, MediaScribeResult)
    assert result.detected_language == "en"
    assert result.full_text == "Hello world."
    assert result.duration_seconds == 1.5
    assert len(result.segments) == 1
    assert result.file_id == str(input_file)
    
    mock_mlx_whisper.transcribe.assert_called_once()
