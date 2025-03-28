from ...abc.backend import AbstractBackend
from ....hystruct import Struct, BinStructBase
from ....hycore import builtin_types


class Binstruct_Backend(AbstractBackend):
    serializer = Struct()
    support_types = (BinStructBase, builtin_types)

    def save(self):
        with self._io.open(self.file, 'wb') as f:
            f.write(self.serializer.dumps(self._data))

    def load(self):
        with self._io.open(self.file, 'rb') as f:
            try:
                if f.size:
                    self.existing = True
                    self.init(**self.serializer.loads(f.read(), mini=True))
            except RuntimeError as e:
                return
