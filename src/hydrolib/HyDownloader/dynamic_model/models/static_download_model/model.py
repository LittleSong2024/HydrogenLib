from numba import int64, List, Tuple
from numba import njit

from .requirements import Task,
from ...model_abc import AbstractDynamicModel


@njit
def size_assign(total: int64, max_chunks: int64, chunk_min_size: int64 = 1024) -> List[Tuple[int64, int64]]:
    if chunk_min_size * max_chunks > total:
        ans = List(Tuple((int64, int64)))
        pos = 0
        while total:
            if chunk_min_size > total:
                pos += total
                total = 0
            else:
                pos += chunk_min_size
                total -= chunk_min_size

            ans.append((pos, pos + chunk_min_size - 1))
    else:
        chunk_size = total // max_chunks
        ans = List()
        for i in range(max_chunks - 1):
            ans.append((i * chunk_size, (i + 1) * chunk_size - 1))
        ans.append(((max_chunks - 1) * chunk_size, total - 1))

    return ans


class Model(AbstractDynamicModel):
    callback_metaclass: CallbackMetaclass

    def __init__(self, callback_metaclass):
        # super().__init__()
        self._assign = None
        self.assigned = False
        self.total_size = callback_metaclass.get_total_size()
        self.assign_policy = callback_metaclass.get_assign_policy()
        self.tasks = []  # type: list[Task]

    def update(self) -> None:
        if not self.assigned:
            self.assigned = True
            # Static assign
            self._assign = size_assign(
                self.total_size,
                self.assign_policy.max_chunk_count,
                self.assign_policy.chunk_min_size
            )
            for assign in self._assign:
                task = self.callback_metaclass.create_task(*assign)
                self.tasks.append(task)
        else:
            for task in self.tasks:
                if task.completed_size == task.end - task.start + 1:
                    self.tasks.remove(task)
            if len(self.tasks) == 0:
                self.stop()
