import jsonpickle
from . import _json


class JsonPickle(_json.Json):
    backend = jsonpickle

