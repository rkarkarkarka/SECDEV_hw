from __future__ import annotations

from collections import deque
from time import monotonic
from typing import Deque, Dict


class RateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self._buckets: Dict[str, Deque[float]] = {}

    def _cleanup(self, key: str, now: float) -> None:
        bucket = self._buckets.get(key)
        if not bucket:
            return
        while bucket and now - bucket[0] > self.window:
            bucket.popleft()
        if not bucket:
            self._buckets.pop(key, None)

    def is_blocked(self, key: str) -> bool:
        now = monotonic()
        self._cleanup(key, now)
        bucket = self._buckets.get(key)
        return bool(bucket) and len(bucket) >= self.limit

    def hit(self, key: str) -> None:
        now = monotonic()
        bucket = self._buckets.setdefault(key, deque())
        self._cleanup(key, now)
        bucket.append(now)

    def reset(self, key: str) -> None:
        self._buckets.pop(key, None)
