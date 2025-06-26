from abc import ABC, abstractmethod, ABCMeta
import ctypes

class CDataMeta(ABCMeta):
    __data__ = ...
    __ctype__ = ...

    def __mul__(cls, other):
        return cls.__ctype__ * other


class AbstractCData(metaclass=CDataMeta):
    """
    抽象基类，代表 ctypes 数据类型的通用行为。
    """

    @classmethod
    @abstractmethod
    def from_buffer(cls, source, offset=0):
        """
        从可写缓冲区创建共享内存的 ctypes 实例。

        :param source: 支持可写缓冲区接口的对象。
        :param offset: 缓冲区内的偏移量，默认为零。
        :raises ValueError: 如果源缓冲区不够大。
        """
        pass

    @classmethod
    @abstractmethod
    def from_buffer_copy(cls, source, offset=0):
        """
        从可读缓冲区拷贝数据以创建 ctypes 实例。

        :param source: 支持可读缓冲区接口的对象。
        :param offset: 缓冲区内的偏移量，默认为零。
        :raises ValueError: 如果源缓冲区不够大。
        """
        pass

    @classmethod
    @abstractmethod
    def from_address(cls, address):
        """
        使用指定地址的内存创建 ctypes 实例。

        :param address: 内存地址，必须是一个整数。
        """
        pass

    @abstractmethod
    def convert(self):
        """
        将对象转换为 ctypes 可识别的类型

        :return: ctypes 可识别的类型
        """
        pass

    @property
    def _b_base_(self):
        """
        获取根 ctypes 对象，该对象拥有当前实例所共享的内存块。

        :return: 根 ctypes 对象。
        """
        return self._b_base_

    @property
    def _b_needsfree_(self):
        """
        判断当前实例是否分配了内存块。

        :return: 布尔值，表示是否需要释放内存。
        """
        return self.__data__._b_needsfree_

    @property
    def _objects(self):
        """
        获取需要保持存活的 Python 对象集合。

        :return: 包含相关对象的字典。
        """
        return self.__data__._objects
