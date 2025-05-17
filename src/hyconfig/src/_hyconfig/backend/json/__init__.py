from ...abc.backend import AbstractBackend
from ....hystruct import *
from ....hycore import json_types


class Json_Backend(AbstractBackend):
    serializer = Json()
    support_types = (json_types, )

    def save(self):
        with self._io.open(self.file, 'wb') as f:
            f.write(self.serializer.dumps(self._data))

    def load(self):
        with self._io.open(self.file, 'rb') as f:
            if f.size:
                self.existing = True
                dic = self.serializer.loads(f.read())
                self.init(**dic)
