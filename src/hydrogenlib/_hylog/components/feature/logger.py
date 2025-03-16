from ..base.level import Level
from ..base.abstracts import LoggingData
from ..methods.handler_manager import *
from ..methods.filter_manager import *
from ..base.formatter import Formatter

from ...._hycore.type_func import get_called_func


class Logger:
    def __init__(self, name):
        self.name = name
        self.handler = HandlerManager()
        self.filter = FilterManager()
        self.formatter = Formatter()
        self.level = Level()

    def set_level(self, level):
        self.level.set(level)

    def add_handlers(self, *handlers):
        self.handler.add_handlers(*handlers)

    def remove_handlers(self, *handlers):
        self.handler.remove_handlers(*handlers)

    def add_filter(self, *filters):
        self.filter.add_filters(*filters)

    def remove_filter(self, *filters):
        self.filter.remove_filters(*filters)

    def set_formatter(self, formatter):
        self.formatter = formatter

    def _do_log(self, level, message, func, *args, **kwargs):
        if self.level >= level:
            data = LoggingData(
                self.name,
                level,
                message,
                func,
                args,
                kwargs
            )
            if self.filter.filter(data):
                self.handler.call(data)

    def _log(self, level, message, *args, **kwargs):
        func = get_called_func(2)
        self._do_log(level, message, func, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self._log('DEBUG', message, *args, **kwargs)

    # TODO: 完成剩余的函数, 完成结构化logger实现

