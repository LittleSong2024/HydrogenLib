from .abstracts import AbstractFormatter, LoggingData


class Formatter(AbstractFormatter):
    def format(self, data: LoggingData):
        return f'{data.timestamp}: [{data.level}] {data.message}'
