# MediaScribe Task Tracker

## Phase 1: Core Foundation (Extraction & Transcription)
- [x] Initialize Python Virtual Environment & install requirements (`mlx-whisper`, `ffmpeg-python`, `pydantic`, `structlog`)
- [x] Implement robust logging setup (`structlog` JSON formatter)
- [x] Implement `AudioExtractor` (Using `ffmpeg` via python)
- [x] Implement audio chunking logic for large files ensuring no OOM memory spikes 
- [x] Implement MLX Whisper Service to infer STT text & Identify Language for audio paths
- [x] Finalize Stage 1 Pydantic structures (`MediaScribeResult`, `TranscriptSegment`)
- [x] Write Unit tests for logic and file format validation
- [x] Write Integration test mocking a small `.mp4` into transcript

## Phase 2: Refinement (Noise Control & Error Handling)
- [ ] Install and wrap `noisereduce` logic around extracted audio arrays pre-transcription
- [ ] Fine-tune inference params (`condition_on_previous_text=False`) against hallucinatory repeats
- [ ] Abstract code into rigorous Try/Except wrapper classes
- [ ] Add `@timeout` mechanisms to stall sub-processes
- [ ] Write Unit and Integration tests for memory bounds and timeouts

## Phase 3: Future Analysis Data Pipelines (Schema Finalization)
- [ ] Add word-level timings and performance metrics into existing models
- [ ] Formally setup `.json` log dumps and DB ingestible schema serializers
- [ ] Write schema integrity unit tests

## Phase 4: Summarization & Translation Plugins (Extensions) 
- [ ] Integrate local `ollama` endpoints and LLaMA 3.2 summarization prompts 
- [ ] Implement `translation` mechanisms
- [ ] Validate Ollama data mappings using integration tests
