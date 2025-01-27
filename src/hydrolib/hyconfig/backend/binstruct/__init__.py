from ...abc.backend import BackendABC
from ....hystruct.Serializers import Struct, BinStructBase


class Binstruct_Backend(BackendABC):
    def __init__(self):
        super().__init__()
        self.serializer = Struct()

    def save(self):
        binstruct = BinStructBase.to_struct(self, ['dic'])
        with self.fd.open(self.file, 'wb') as f:
            f.write(self.serializer.dumps(binstruct))

    def load(self):
        with self.fd.open(self.file, 'rb') as f:
            try:
                if f.size:
                    struct = self.serializer.loads(f.read(), __data__=['dic'])
                    # print("aaa", struct)
                    self.init(**struct.dic)

                    self.is_first_loading = False
            except RuntimeError as e:
                return
