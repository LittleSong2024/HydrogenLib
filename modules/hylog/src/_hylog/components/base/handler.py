from .abstracts import AbstractHandler, LoggingData


class Handler(AbstractHandler):
    def handle(self, message, data: LoggingData):
        print(message)
