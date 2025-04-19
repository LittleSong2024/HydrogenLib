from abc import ABC, abstractmethod


class AbstractMarker(ABC):
    @abstractmethod
    def generate(self, countainer, **kwargs):
        """
        为标记生成一个确切的值
        :param countainer:父容器
        :param kwargs: 外部传入的额外参数
        :return: Any
        """

