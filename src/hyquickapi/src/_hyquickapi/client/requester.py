import requests

from .api_abc import API_Requester


class BasicRequester(API_Requester):
    def request(self, method, url, data: dict) -> tuple[int, dict]:
        response = requests.request(method, url, data=data)
        return response.status_code, response.json()
