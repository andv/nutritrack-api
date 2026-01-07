# src/utils/rate_limit.py
import time
import asyncio
from functools import wraps
from typing import Optional

class RateLimiter:
    def __init__(self, delay: float = 1.0):
        self.interval = 1.0 / delay
        self.last_call = 0.0

    def wait(self):
        """Ждёт, если нужно, чтобы не превысить лимит."""
        now = time.time()
        elapsed = now - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.time()

# Удобный декоратор
def rate_limited(calls_per_second=1.0):
    limiter = RateLimiter(calls_per_second)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter.wait()
            return func(*args, **kwargs)
        return wrapper
    return decorator


class AsyncRateLimiter:
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_call: Optional[float] = None

    async def __aenter__(self):
        now = asyncio.get_event_loop().time()
        if self.last_call is not None:
            elapsed = now - self.last_call
            if elapsed < self.delay:
                await asyncio.sleep(self.delay - elapsed)
        self.last_call = asyncio.get_event_loop().time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass