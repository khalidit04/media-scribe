import time
import pytest
from media_scribe.utils import timeout
from media_scribe.exceptions import TranscriptionTimeoutError

def test_timeout_decorator_success():
    @timeout(2)
    def fast_function():
        return "success"
        
    assert fast_function() == "success"

def test_timeout_decorator_failure():
    @timeout(1)
    def slow_function():
        time.sleep(2)
        return "too late"
        
    with pytest.raises(TranscriptionTimeoutError):
        slow_function()
