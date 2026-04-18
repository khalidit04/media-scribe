import os
from media_scribe.schemas import MediaScribeResult, TranscriptSegment
from media_scribe.core import export_to_json

def test_json_export(tmp_path):
    result = MediaScribeResult(
        file_id="test.mp4",
        original_format="mp4",
        detected_language="en",
        duration_seconds=5.0,
        full_text="Hello world.",
        segments=[
            TranscriptSegment(
                start_time=0.0,
                end_time=5.0,
                text="Hello world."
            )
        ],
        processing_time_ms=100
    )
    
    output_file = tmp_path / "output.json"
    export_to_json(result, str(output_file))
    
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        content = f.read()
        assert "Hello world." in content
