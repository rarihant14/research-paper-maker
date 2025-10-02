
import functools
import os

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

def track_with_langsmith(func):
    """Minimal decorator that logs entry/exit. Replace with LangSmith SDK when ready."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        job_id = args[0] if args else kwargs.get("job_id")
        if LANGSMITH_API_KEY and job_id:
            print(f"[LangSmith] start job {job_id} - {func.__name__}")
        result = await func(*args, **kwargs)
        if LANGSMITH_API_KEY and job_id:
            print(f"[LangSmith] end job {job_id} - {func.__name__}")
        return result
    return wrapper
