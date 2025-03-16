from ...._hycore.utils import Dotpath


class LoggerKey:
    def __init__(self, logger):
        self.logger = logger
        self.path = Dotpath()


class LoggerRegister:
    def __init__(self):
        self.loggers = {}
