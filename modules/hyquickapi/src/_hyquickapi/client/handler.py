from .api_abc import API_Handler
from ..._hycore.type_func import AttrDict


class ObjectiveJsonHandler(API_Handler):
    def handle(self, api, status_code, response):
        for key, value in list(response.items()):
            if isinstance(value, dict):
                self.handle(None, status_code, value)
                response[key] = AttrDict(**value)
        return response
