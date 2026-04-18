"""
Modular plugin architecture for NLP extensions (Summarization & Translation).
"""
import json
from abc import ABC, abstractmethod
import requests
from media_scribe.schemas import ContentSummary
from media_scribe.logger import logger
from media_scribe.utils import timeout

class BaseNLPProvider(ABC):
    """
    Abstract base class for NLP providers.
    Allows swapping between local LLMs (Ollama) and cloud APIs (OpenAI).
    """
    @abstractmethod
    def summarize(self, text: str) -> ContentSummary:
        """Abstract method for text summarization."""

    @abstractmethod
    def translate(self, text: str, target_lang: str) -> str:
        """Abstract method for text translation."""

class OllamaProvider(BaseNLPProvider):
    """
    Implementation of NLP provider using a local Ollama instance.
    """
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3.2"):
        self.host = f"{host.rstrip('/')}/api/generate"
        self.model = model

    @timeout(120)
    def summarize(self, text: str) -> ContentSummary:
        """Generates a summary using the configured LLM provider."""
        logger.info(f"Summarizing via {self.__class__.__name__}", model=self.model)
        prompt = (
            "Analyze the transcript and return a JSON object with 'gist' (string) "
            "and 'key_points' (list of strings).\n\n"
            f"Transcript: {text}"
        )
        try:
            response = requests.post(
                self.host,
                json={"model": self.model, "prompt": prompt, "stream": False, "format": "json"},
                timeout=110
            )
            response.raise_for_status()
            content = json.loads(response.json().get("response", "{}"))
            return ContentSummary(
                gist=content.get("gist", "No summary generated."),
                key_points=content.get("key_points", [])
            )
        except (requests.RequestException,
                json.JSONDecodeError, KeyError) as e:
            logger.error(f"{self.__class__.__name__} failed", error=str(e))
            return ContentSummary(gist="Summary generation failed.", key_points=[])

    @timeout(120)
    def translate(self, text: str, target_lang: str) -> str:
        """Translates text using the configured LLM provider."""
        logger.info(f"Translating via {self.__class__.__name__}", model=self.model, target=target_lang)
        prompt = f"Translate the following text to {target_lang}. Return ONLY the translation:\n\n{text}"
        try:
            response = requests.post(
                self.host,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=110
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except requests.RequestException as e:
            logger.error("Ollama translation failed", error=str(e))
            return f"Translation failed: {str(e)}"
