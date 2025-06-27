from ...abc.backend import AbstractBackend
from ...abc.model import AbstractModel
from _hycore.json import json_types
import json


class Json_Backend(AbstractBackend):
    serializer = json
    __support_types__ = (json_types,)

    def __init__(self):
        self.model: AbstractModel = None

    def set_model(self, model):
        self.model = model
        return self

    def get_model(self):
        return self.model

    def save(self, file):
        with open(file, 'w') as (f):
            json.dump(self.model.data, f)

    def load(self, file):
        with open(file, 'r') as (f):
            self.model.init(json.load(f))
