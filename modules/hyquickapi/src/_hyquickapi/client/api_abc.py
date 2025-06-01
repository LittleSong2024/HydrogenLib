from abc import *
from typing import Any

from attr import s, ib


@s
class SerializedData:
    data = ib()
    argument = ib('json')
    mime_type = ib('application/json')


class API_ValueItem(ABC):
    """
    API 元素基类
    应该重写 generate 方法
    """

    def generate(self, api, **kwargs):
        ...


def transform(obj, api, **kwargs):
    if isinstance(obj, API_ValueItem):
        return obj.generate(api, **kwargs)
    else:
        return obj


class API_Serializer(ABC):
    @abstractmethod
    def serialize(self, api, **kwargs) -> SerializedData:
        ...

    @abstractmethod
    def deserialize(self, api, **kwargs) -> Any:
        ...


class API_Requester(ABC):
    @abstractmethod
    def request(self, method, url, serialized_data: SerializedData) -> tuple[int, Any]:
        """
        :param method: 请求方法 (Get|Post|Put|Delete)
        :param url: 请求地址
        :param serialized_data: 请求数据
        :return: 返回错误码和返回数据
        """
        ...


class API_Handler(ABC):
    @abstractmethod
    def handle(self, api, status_code, response):
        ...


class API_Backend:
    api_serializer = None
    api_requester = None
    api_handlers = None

    def run(self, api, request_template, method, payload, kwargs):
        payload = request_template.generate(api, **kwargs)  # 先生成请求数据
        payload = self.api_serializer.serialize(payload, **kwargs)  # 对初始的数据进行序列化
        return

    def load(self, response_template, ):
        ...


class API_ResponseCase(ABC):
    @abstractmethod
    def check(self, status_code, response):
        ...

    @abstractmethod
    def __hash__(self):
        ...
