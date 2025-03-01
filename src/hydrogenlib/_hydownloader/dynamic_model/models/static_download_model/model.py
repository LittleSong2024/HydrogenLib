import time

from .requirements import Task, CallbackMetaclass
from ...model_abc import AbstractDynamicModel


def size_assign(total, max_chunks, chunk_min_size = 1024):
    ans = []
    chunk_size = max(total // max_chunks, chunk_min_size)
    for i in range(max_chunks - 1):
        ans.append((i * chunk_size, (i + 1) * chunk_size - 1))
    ans.append(((max_chunks - 1) * chunk_size, total - 1))
    return ans

def reassign_calc(task: Task):
    speed = task.completed_size / (time.time() - task.start_time)
    total = task.end - task.start + 1
    size = (total - speed * task.connect_time) / 2
    return task.start + int(size)  # 重分配点


class Model(AbstractDynamicModel):
    callback_metaclass: CallbackMetaclass

    def __init__(self, callback_metaclass):
        # super().__init__()
        self._assign = None
        self.total_size = callback_metaclass.get_total_size()
        self.assign_policy = callback_metaclass.get_assign_policy()
        self.tasks = []  # type: list[Task]

    def init(self):
        super().init()
        # Static assign
        self._assign = size_assign(
            self.total_size,
            self.assign_policy.max_chunk_count,
            self.assign_policy.chunk_min_size
        )
        for assign in self._assign:
            task = self.callback_metaclass.create_task(*assign)
            self.tasks.append(task)

    def update(self) -> None:
        for task in self.tasks:
            if task.completed_size == task.end - task.start + 1:
                self.tasks.remove(task)
        if len(self.tasks) == 0:
            self.stop()
