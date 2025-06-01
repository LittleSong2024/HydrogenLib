from .api_abc import *
from ..._hycore.type_func import template_match


class RequestTemplate:
    def __init__(self, dct):
        self.dct = dct

    def process(self, dct, api, kwargs):
        for key, value in list(dct.items()):
            if isinstance(value, dict):
                self.process(value, api, kwargs)
            else:
                dct[key] = transform(value, api, **kwargs)

    def generate(self, api, kwargs):
        dct = self.dct.copy()
        self.process(dct, api, kwargs)
        return dct


class ResponseTemplate:
    def __init__(self, dct):
        self.dct = dct

    def process(self, dct):
        if not template_match(dct, self.dct):
            raise ValueError("Response data is not match with template")

    def generate(self, rps_code, rps_data) -> dict:
        self.process(rps_data)
        return rps_data
