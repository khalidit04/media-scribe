import sys
sys.path.insert(0, "./src")  # This allows it to find the media_scribe package easily!
from media_scribe.core import process_media

def test_video(video_path: str):
    print(f"Testing MediaScribe on: {video_path}")
    print("This will run extraction -> noise reduction -> MLX-Whisper transcription.")
    print("-------------------------------------------------------------------------")
    
    try:
        # Run the full pipeline with our newly added clean_audio feature
        result = process_media(
            file_path=video_path,
            clean_audio=True
        )
        
        print("\n=== SUCCESS ===")
        print(f"Detected Language: {result.detected_language}")
        print(f"Total Audio Duration: {result.duration_seconds:.2f}s")
        print(f"Total Processing Time: {result.processing_time_ms}ms")
        print("\nFull Transcript:")
        print("----------------")
        print(result.full_text)
        
    except Exception as e:
        print(f"\n=== FAILURE ===")
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_on_video.py <path_to_video_file>")
        sys.exit(1)
        
    test_video(sys.argv[1])
