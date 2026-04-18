import functools
import concurrent.futures
from media_scribe.exceptions import TranscriptionTimeoutError

def timeout(seconds: int):
    """
    Decorator that enforces a strict timeout on synchronous functions.
    Raises TranscriptionTimeoutError if the timeout is exceeded.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use ThreadPoolExecutor to run the function and enforce a timeout.
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except concurrent.futures.TimeoutError:
                    # Reraise as our custom timeout error
                    raise TranscriptionTimeoutError(
                        f"Execution of {func.__name__} timed out after {seconds} seconds."
                    )
        return wrapper
    return decorator
