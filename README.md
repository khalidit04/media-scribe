# Media Scribe

Media Scribe is a Python library for processing large audio/video files. It automates media format normalization, performs accurate multi-language transcription with noise reduction, and establishes a structured, log-heavy, and error-resilient pipeline.

## Project Structure & Development Methodology

This project follows a **Specification-Driven Development (SDD)** pattern:

- **`spec/`**: Contains the full specification and architectural documents for the system. Check the `spec` folder to understand the requirements, design, and architecture before referring to the code.
- **`spec/phased-task.md`**: Provides a step-by-step roadmap indicating that this library will be implemented in a phased manner.
- **Iterative Implementation**: The codebase implementation is iterative and closely adheres to the specifications and phased tasks defined in the `spec` folder.

## Installation

As the library is currently under active development, you can install the dependencies via `requirements.txt`:

```bash
git clone https://github.com/khalidit04/media-scribe.git
cd media-scribe
pip install -r requirements.txt
```

*(Note: Once published, installation will be a simple `pip install media-scribe`)*

## Quickstart

```python
from media_scribe.core import process_media

# Run the end-to-end extraction and transcription pipeline
result = process_media(
    file_path="video.mp4",
    
    # [Optional] Defaults to 'mlx-community/whisper-small-mlx'. 
    # Use 'mlx-community/whisper-large-v3-mlx' for state-of-the-art Arabic/Urdu accuracy.
    model_size="mlx-community/whisper-small-mlx", 
    
    # [Optional] Defaults to False. 
    # Set to True to mathematically remove background static/hum before transcription!
    clean_audio=True 
)

# The pipeline returns a strictly typed Pydantic object with rich metadata:
print(f"Detected Language: {result.detected_language}")
print(f"Total Audio Duration: {result.duration_seconds}s")
print(f"Total Processing Time: {result.processing_time_ms}ms")

# Access the full block of text, or iterate over result.segments for precise timings
print("\nTranscript:")
print(result.full_text)
```

## Contributing

We welcome contributions! Because this project is specification-driven:
1. Please thoroughly review the documents in the `spec/` folder.
2. Ensure any new features or architectures align with the existing `implementation_plan.md` and `phased-task.md`.
3. Open an issue to discuss significant changes before submitting a Pull Request.
