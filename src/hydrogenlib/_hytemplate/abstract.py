from abc import ABC

from .._hycore.utils import AutoSingleton


class AbstractMarker(ABC):
    def generate(self, countainer, **kwargs):
        """
        为标记生成一个确切的值
        :param countainer:父容器
        :param kwargs: 外部传入的额外参数
        :return: Any
        """

    def restore(self, countainer, value, **kwargs):
        """
        把值还原成标记
        :param countainer:父容器
        :param kwargs: 外部传入的额外参数
        """


def generate(marker_or_any, countainer, **kwargs):
    if isinstance(marker_or_any, AbstractMarker):
        return marker_or_any.generate(countainer, **kwargs)
    else:
        return marker_or_any


def restore(marker_or_any, countainer, value, **kwargs):
    if isinstance(marker_or_any, AbstractMarker):
        return marker_or_any.restore(countainer, value, **kwargs)
    else:
        return marker_or_any
