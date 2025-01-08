from typing import *


@runtime_checkable
class Task(Protocol):
    start: int
    end: int
    completed_size: int
    start_time: float


@runtime_checkable
class Policy(Protocol):
    chunk_min_size: int
    max_chunk_count: int


@runtime_checkable
class CallbackMetaclass(Protocol):
    def create_task(self, start: int, end: int) -> Task: ...

    def get_total_size(self) -> int: ...

    def get_assign_policy(self) -> Policy: ...
