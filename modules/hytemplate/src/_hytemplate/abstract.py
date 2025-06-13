from abc import ABC


class AbstractMarker(ABC):
    def generate(self, context):
        """
        为标记生成一个确切的值
        """

    def restore(self, context):
        """
        把值还原成标记
        """
