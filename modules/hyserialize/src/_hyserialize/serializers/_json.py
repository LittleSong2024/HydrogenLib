import json
from . import abstract


class Json(abc.AbstractSerializer):
    backend = json
    
    def dump(self, fp, *args, **kwargs):
        return self.backend.dump(fp, *args, **kwargs)

    def load(self, fp, *args, **kwargs):
        return self.backend.load(fp, *args, **kwargs)

    def dumps(self, data, *args, **kwargs):
        return self.backend.dumps(data, *args, **kwargs).encode()

    def loads(self, data, *args, **kwargs):
        return self.backend.loads(data, *args, **kwargs)
    