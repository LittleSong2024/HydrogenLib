from abc import ABC, abstractmethod


class AbstractCondition(ABC):
    @abstractmethod
    def run(self, template, **kwargs) -> bool:
        """
        运行条件检查
        :param template: 顶层模版实例
        :param kwargs: 生成参数
        :return: 检查结果,通常为bool类型
        """
