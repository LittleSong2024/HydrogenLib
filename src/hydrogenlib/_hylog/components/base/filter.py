from typing import Union

from .abstracts import AbstractFilter, LoggingData
from .level import Level


class Filter(AbstractFilter):
    def __init__(self):
        self.level = Level()

    def set_level(self, level: Union[Level, int, str]):
        self.level.set(level)

    def filter(self, message, data: LoggingData):
        return True
