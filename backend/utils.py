import time
import functools
from collections import deque

class RateLimiter:
    def __init__(self, max_calls: int, period: float = 1.0):
        self.max_calls = max_calls
        self.period = period
        self.timestamps = deque()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove timestamps older than the period
            while self.timestamps and now - self.timestamps[0] > self.period:
                self.timestamps.popleft()
            
            if len(self.timestamps) >= self.max_calls:
                sleep_time = self.timestamps[0] + self.period - now
                if sleep_time > 0:
                    time.sleep(sleep_time)
                # Re-check time after sleeping
                now = time.time()
                while self.timestamps and now - self.timestamps[0] > self.period:
                    self.timestamps.popleft()

            self.timestamps.append(time.time())
            return func(*args, **kwargs)
        return wrapper
