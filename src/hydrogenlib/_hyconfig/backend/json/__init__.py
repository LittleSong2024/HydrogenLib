from ...abc.backend import BackendABC
from ....hystruct import *
from ....hycore import json_types


class Json_Backend(BackendABC):
    serializer = Json()
    support_types = (json_types, )

    def save(self):
        with self._fd.open(self.file, 'wb') as f:
            f.write(self.serializer.dumps(self._data))

    def load(self):
        with self._fd.open(self.file, 'rb') as f:
            if f.size:
                self.existing = True
                dic = self.serializer.loads(f.read())
                self.init(**dic)
