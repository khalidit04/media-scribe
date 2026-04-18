# MediaScribe: Technical Specification & Implementation Plan

This document outlines the technical specification, architecture, and phase-by-phase implementation plan for **MediaScribe**, a robust Python-based audio and video processing library. 

## 1. System Overview & Objectives
MediaScribe is designed to process large audio/video files, extract and clean the audio layer, identify the spoken language (e.g., Arabic, Urdu, Hindi, English), and generate an accurate text transcription. It also sets the foundation for advanced NLP features like summarization and translation.

## 2. Core Requirements & Technology Stack

### 2.1 File Format Handling (Extensible & Configurable)
- **Tooling:** `ffmpeg-python` (requires system `ffmpeg` installation via Homebrew)
- **Approach:** Standardize all incoming media variants (`.mp4`, `.flv`, `.wav`, `.m4a`, etc.) by extracting their audio streams and converting them to a uniform uncompressed format (e.g., standard `16kHz`, `mono` WAV).

### 2.2 Language Identification & Transcription (Apple Silicon Optimized)
- **Hardware Constraint Context:** Mac Mini M4 with 16GB RAM (No external GPU, but features highly capable Apple Silicon Unified Memory).
- **Tooling:** Apple's `mlx-whisper` or `whisper.cpp` Python bindings.
- **Approach:** Standard Whisper or `faster-whisper` relies heavily on NVIDIA GPUs (CUDA). Since we are running on an Apple M4 chip with 16GB RAM, we will utilize Apple's MLX Machine Learning framework (`mlx-whisper`), which is precision-engineered to run Whisper extremely fast using the Mac's unified memory and neural engine, without exceeding the 16GB memory bound.

### 2.3 Audio Clean-up (Noise & Repetition Removal)
- **Acoustic Noise Removal:** Use `noisereduce` (spectral gating).
- **Transcribed Noise/Repetition:** Configurable inference parameters (`condition_on_previous_text=False`, `compression_ratio_threshold`) to skip silent/noisy chunks and avoid text hallucination loops.

### 2.4 Handling Large Files (Chunking & Memory)
- **Tooling:** `pydub` or native `ffmpeg` slicing.
- **Approach:** To adhere properly to the 16GB RAM limit, large video/audio inputs will be loaded and transcribed in sliding windows/chunks (e.g., 5 to 10-minute segments). Memory will be eagerly garbage-collected between chunks.

### 2.5 Error Handling & Timeouts
- **Approach:** 
  - Custom exceptions (`MediaExtractionError`, `TranscriptionTimeoutError`, `LanguageNotSupportedError`).
  - Use Python's `asyncio.wait_for` or threaded `concurrent.futures` to enforce strict timeouts on hanging sub-processes.

### 2.6 Logging Strategy
- **Tooling:** Python's built-in `logging` module combined with `structlog`.
- **Approach:** Generate JSON-formatted logs ensuring key traceability (e.g., include `file_name`, `chunk_id`, `process_duration`, `ram_usage`).

### 2.7 Extensible Output Schema
- **Tooling:** `pydantic`
- **Approach:** Strictly typed JSON schemas for outputs ensures future databases or API endpoints can reliably consume the transcriptions.

## 3. Phased Implementation Plan with Testing Strategies

### Phase 1: Core Foundation (Extraction & Transcription)
- **Features:**
  - Establish Python project structure and `structlog` logging framework.
  - Implement the `AudioExtractor` layer using `ffmpeg`.
  - Implement memory-safe chunking for large files.
  - Integrate M4-optimized `mlx-whisper` for Speech-to-Text and Language Detection.
  - Draft basic Pydantic output schemas.
- **Testing:**
  - **Unit Tests:** Mock `ffmpeg` calls and assert that configurations parse correctly. Mock the MLX inference engine to ensure chunk stitching logic works perfectly.
  - **Integration Tests:** Execute an end-to-end extraction and transcription on a sample 30-second `.mp4` file to confirm valid transcription output.

### Phase 2: Refinement (Noise Control & Error Handling)
- **Features:**
  - Apply `noisereduce` dynamically on extracted audio arrays before passing to Whisper.
  - Post-process text using generic deduplication functions.
  - Wrap logic in custom Exception handlers (`MediaExtractionError`, etc.).
  - Implement system-wide `@timeout` limits.
- **Testing:**
  - **Unit Tests:** Test the audio-cleaning algorithm by feeding an array of simulated static noise. Test `timeout` decorators by simulating a stalled thread.
  - **Integration Tests:** Process heavily distorted audio samples and verify the transcription quality improves over Phase 1. Force a timeout limit of 1 second on a large file and ensure a `TranscriptionTimeoutError` is gracefully caught, triggering no overall system crash.

### Phase 3: Future Analysis Data Pipelines (Schema Finalization)
- **Features:**
  - Expand Pydantic schemas to include word-level timestamps, execution duration metadata, and memory utilization statistics.
  - Export final structure directly into flat JSON logs or database-ready dumps.
- **Testing:**
  - **Unit Tests:** Validate raw Python dictionaries against `pydantic` schema validators to ensure invalid records throw `ValidationError`.
  - **Integration Tests:** Verify that writing thousands of chunk records into JSON works without corrupting the file syntax.

### Phase 4: Summarization & Translation Plugins
- **Features:**
  - **Summarization:** Use `ollama` running locally on the Mac M4 (using e.g., `llama3.2` or `mistral`) to generate a gist/summary. The local MLX models and Ollama are both highly optimized for Apple Silicon.
  - **Translation:** Target translation via locally hosted models or via Whisper's built-in `translate` task.
- **Testing:**
  - **Unit Tests:** Mock Ollama API responses to test correct mapping of the summary property into the Pydantic schema.
  - **Integration Tests:** Verify connection latency and local API handshakes between MediaScribe and the Ollama service using real but short text strings.

## 4. Final Output Schema Design

```python
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
```
