from ...abc.backend import BackendABC
from ....hystruct.Serializers import Struct, BinStructBase


class Binstruct_Backend(BackendABC):
    def __init__(self):
        super().__init__()
        self.serializer = Struct()

    def save(self):
        binstruct = BinStructBase.to_struct(self, ['dic', 'defaults'])
        with self.fd.open(self.file, 'b') as f:
                f.write(self.serializer.dumps(binstruct))

    def load(self):
        with self.fd.open(self.file, 'b') as f:
            if f.size:
                self.is_first_loading = False
                struct = self.serializer.loads(f.read())
                self.init(**struct.dic)
                self.set_defaults(**struct.defaults)

