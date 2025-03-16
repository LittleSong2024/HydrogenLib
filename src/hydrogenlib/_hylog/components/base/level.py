from src.hydrogenlib._hycore.utils import DoubleDict


class Level:
    level_mapping = DoubleDict({
        "DEBUG": 0,
        "INFO": 1,
        "WARNING": 2,
        "ERROR": 3,
        "CRITICAL": 4,
        "NOTSET": 5,
        "FATAL": 6,
        "ALERT": 7,
        "EMERGENCY": 8,
        "PANIC": 9,
        "FATALITY": 10,
    })

    def __init__(self, name_or_int=5):
        self.name = 'NOTSET'
        self.level = 5

        self.set(name_or_int)

    def set(self, name_or_int):
        if isinstance(name_or_int, str):
            self.name = name_or_int
            self.level = self.level_mapping.get(name_or_int, 5)

        elif isinstance(name_or_int, int):
            self.level = name_or_int
            self.name = self.level_mapping.get(name_or_int, 'UNKNOWN')

        elif isinstance(name_or_int, Level):
            self.name = name_or_int.name
            self.level = name_or_int.level

    def __str__(self):
        return f'{self.name}({self.level})'

    def __eq__(self, other):
        return self.level == other.level

    def __ne__(self, other):
        return self.level != other.level

    def __hash__(self):
        return hash(self.level)

    def __lt__(self, other):
        return self.level < other.level

    def __le__(self, other):
        return self.level <= other.level

    def __gt__(self, other):
        return self.level > other.level

    def __ge__(self, other):
        return self.level >= other.level

    __repr__ = __str__
