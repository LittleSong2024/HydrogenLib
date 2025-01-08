from .model_abc import *
from ...utils.Clock import Clock


class Runner:
    """
    将模型和执行器绑定,按照指定频率刷新模型
    """
    def __init__(self, model: AbstractDynamicModel = None, executor: AbstractExecutor = None):
        self.model = model
        self.executor = executor
        self.clock = Clock()
        self._running = True

    def set_model(self, model: AbstractDynamicModel):
        self.model = model

    def set_executor(self, executor: AbstractExecutor):
        self.executor = executor

    def stop(self):
        self._running = False
        self.executor.on_stop()

    def start(self, interval: float = 0.1):
        self.executor.on_run()
        while self._running:
            self.model.update()
            if self.model.running is False:
                self.stop()
            self.clock.strike(interval)
