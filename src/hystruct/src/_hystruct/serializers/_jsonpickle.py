import jsonpickle
from . import _json


class JsonPickle(S_Json.Json):
    def dumps(self, data):
        return jsonpickle.dumps(data).encode()

    def loads(self, data):
        return jsonpickle.loads(data)

