from .api_abc import API_ResponseCase


class Range(API_ResponseCase):
    def __init__(self, a, b):
        self.a, self.b = a, b

    def __hash__(self):
        return hash((self.a, self.b))

    def check(self, status_code, response):
        return self.a <= status_code < self.b


class Default(API_ResponseCase):
    def __hash__(self):
        return hash(None)

    def check(self, status_code, response):
        return True
