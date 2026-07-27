"""Bloqueio simples em memória para reduzir tentativas de força bruta."""

from dataclasses import dataclass
from threading import Lock
from time import monotonic


@dataclass
class AttemptRecord:
    failures: int = 0
    locked_until: float = 0.0


class AttemptLockout:
    def __init__(self) -> None:
        self._records: dict[str, AttemptRecord] = {}
        self._lock = Lock()

    def is_locked(self, identity: str) -> int:
        with self._lock:
            record = self._records.get(identity)
            if record is None or record.locked_until <= monotonic():
                return 0
            return max(1, round(record.locked_until - monotonic()))

    def failure_count(self, identity: str) -> int:
        """Retorna falhas consecutivas ainda ativas, sem expor o registro interno."""
        with self._lock:
            record = self._records.get(identity)
            if record is None or record.locked_until > monotonic():
                return 0
            return record.failures

    def record_failure(self, identity: str, *, max_attempts: int, lockout_seconds: int) -> int:
        with self._lock:
            record = self._records.setdefault(identity, AttemptRecord())
            record.failures += 1
            if record.failures >= max_attempts:
                record.failures = 0
                record.locked_until = monotonic() + lockout_seconds
                return lockout_seconds
            return 0

    def record_success(self, identity: str) -> None:
        with self._lock:
            self._records.pop(identity, None)


attempt_lockout = AttemptLockout()
