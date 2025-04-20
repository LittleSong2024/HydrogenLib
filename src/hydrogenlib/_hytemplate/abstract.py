from abc import ABC


class AbstractMarker(ABC):
    def generate(self, countainer, **kwargs):
        """
        为标记生成一个确切的值
        :param countainer:父容器
        :param kwargs: 外部传入的额外参数
        :return: Any
        """

    def restore(self, countainer, **kwargs):
        """
        把值还原成标记
        :param countainer:父容器
        :param kwargs: 外部传入的额外参数
        """
