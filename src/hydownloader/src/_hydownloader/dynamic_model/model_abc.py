from abc import ABC, abstractmethod


class AbstractDynamicModel(ABC):
    callback_metaclass: object
    running: bool

    @abstractmethod
    def update(self) -> None:
        """
        更新模型
        """
        ...

    def init(self):
        """
        初始化模型
        """
        self.running = True  # 默认初始化功能

    def stop(self):
        """
        停止并释放模型
        """
        self.running = False  # 默认释放功能


class AbstractExecutor(ABC):
    @abstractmethod
    def on_run(self):
        """
        当模型与执行器绑定并被启动时,调用此方法
        """
        ...

    @abstractmethod
    def on_stop(self):
        """
        当模型返回结束消息时,调用此方法
        """
        ...
