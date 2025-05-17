from .handler import ObjectiveJsonHandler
from .requester import BasicRequester
from .api_abc import API_Backend


class JsonBackend(API_Backend):
    api_handlers = ObjectiveJsonHandler()
    api_requester = BasicRequester()
    api_serializer = None
