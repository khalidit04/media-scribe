"""
Tests for audio cleaning and noise reduction logic.
"""
from unittest.mock import patch, MagicMock
import pytest
import numpy as np
from media_scribe.cleaner import apply_noise_reduction
from media_scribe.exceptions import MediaScribeError

@patch("media_scribe.cleaner.os.path.exists")
@patch("media_scribe.cleaner.sf.SoundFile")
@patch("media_scribe.cleaner.nr.reduce_noise")
def test_apply_noise_reduction(mock_reduce_noise, mock_soundfile, mock_exists):
    """
    Test successful noise reduction by mocking soundfile blocks and spectral gating.
    """
    mock_exists.return_value = True

    # Setup mocks for context managers
    mock_in_file = MagicMock()
    mock_in_file.samplerate = 16000
    mock_in_file.channels = 1

    dummy_block = np.zeros((16000, 1))
    mock_in_file.blocks.return_value = [dummy_block]

    mock_out_file = MagicMock()

    # SoundFile is called twice: once for reading, once for writing.
    ctx1 = MagicMock()
    ctx1.__enter__.return_value = mock_in_file
    ctx2 = MagicMock()
    ctx2.__enter__.return_value = mock_out_file

    mock_soundfile.side_effect = [ctx1, ctx2]

    # mock reduce_noise returns an array
    mock_reduce_noise.return_value = np.zeros(16000)

    result = apply_noise_reduction("dummy.wav", chunk_duration_sec=1)

    assert result == "dummy_cleaned.wav"
    mock_reduce_noise.assert_called_once()
    mock_out_file.write.assert_called_once()

def test_apply_noise_reduction_file_not_found():
    """Test that a non-existent file raises MediaScribeError."""
    with pytest.raises(MediaScribeError, match="File not found"):
        apply_noise_reduction("non_existent.wav")
