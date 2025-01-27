from ...abc.backend import BackendABC
from ....hystruct.Serializers import Json


class Json_Backend(BackendABC):
    serializer = Json()

    def save(self):
        with self.fd.open(self.file, 'wb') as f:
            f.write(self.serializer.dumps(self.dic))

    def load(self):
        with self.fd.open(self.file, 'rb') as f:
            if f.size:
                self.is_first_loading = False
                dic = self.serializer.loads(f.read())
                self.init(**dic)
