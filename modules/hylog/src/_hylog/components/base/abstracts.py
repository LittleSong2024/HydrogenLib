from abc import ABC, abstractmethod
import attr

from .level import Level


@attr.s
class LoggingData:
    timestamp = attr.ib(type=float)  # timestamp in seconds
    level = attr.ib(type=Level)  # 'INFO', 'WARNING', 'ERROR', ...
    message = attr.ib(type=str)  # message text
    function = attr.ib(type=str)  # function name
    args = attr.ib(type=tuple)  # args
    kwargs = attr.ib(type=dict)  # kwargs


class AbstractFormatter(ABC):
    @abstractmethod
    def format(self, data: LoggingData): ...


class AbstractHandler(ABC):
    @abstractmethod
    def handle(self, message, data: LoggingData): ...


class AbstractFilter(ABC):
    @abstractmethod
    def filter(self, message, data: LoggingData): ...


