"""
Unit tests for Phase 4 Plugins (Ollama Summarization & Translation).
"""
import json
from unittest.mock import patch, MagicMock
import requests
from media_scribe.plugins import OllamaProvider
from media_scribe.schemas import ContentSummary

@patch("media_scribe.plugins.requests.post")
def test_summarize_success(mock_post):
    """Test successful summarization from mocked Ollama response."""
    # Mock Ollama JSON response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": json.dumps({
            "gist": "This is a gist.",
            "key_points": ["Point 1", "Point 2"]
        })
    }
    mock_post.return_value = mock_response

    provider = OllamaProvider()
    result = provider.summarize("Long transcript text...")

    assert isinstance(result, ContentSummary)
    assert result.gist == "This is a gist."
    assert result.key_points == ["Point 1", "Point 2"]
    mock_post.assert_called_once()

@patch("media_scribe.plugins.requests.post")
def test_translate_success(mock_post):
    """Test successful translation from mocked Ollama response."""
    # Mock Ollama response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Bonjour tout le monde"}
    mock_post.return_value = mock_response

    provider = OllamaProvider()
    result = provider.translate("Hello everyone", target_lang="French")

    assert result == "Bonjour tout le monde"
    mock_post.assert_called_once()

@patch("media_scribe.plugins.requests.post")
def test_ollama_failure_graceful_handling(mock_post):
    """Ensure that plugin returns fallback values if Ollama call fails."""
    mock_post.side_effect = requests.RequestException("Ollama is down")

    provider = OllamaProvider()
    result = provider.summarize("Transcript text")

    assert "failed" in result.gist.lower()
    assert result.key_points == []
