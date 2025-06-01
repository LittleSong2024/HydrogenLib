import json
from . import abc


class Json(abc.AbstractSerializer):
    left_delimiter = b"{["
    right_delimiter = b"}]"

    quotations = b"'\""

    mapping = {
        b'{': b'}',
        b'[': b']',
    }

    def __init__(self):
        self.stack = None
        self.s = None

    def dumps(self, data):
        return json.dumps(data).encode()

    def loads(self, data):
        return json.loads(data)