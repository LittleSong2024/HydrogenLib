from __future__ import annotations

from typing import Type, Any

from .utils.instance_dict import InstanceDict


class BetterDescriptor:
    __better_instance_mapping__: InstanceDict = None
    __better_type__: Type["BetterDescriptorInstance"]

    def get_instance_by_instance(self, instance) -> BetterDescriptorInstance:
        """
        根据实例获取对应的 BetterDescriptorInstance 实例。
        :param instance: 访问描述符的实例。
        :return: 对应 BetterDescriptorInstance 实例的值.
        """
        return self.__better_instance_mapping__.get(instance).value if instance in self.__better_instance_mapping__ else self.__better_new__()

    def __init__(self, *args, **kwargs):
        """
        初始化 BetterDescriptor 实例。
        :param args: 传递给实例化的参数。
        :param kwargs: 传递给实例化的关键字参数。
        """
        self.__better_instance_mapping__ = InstanceDict()
        self.args, self.kwargs = args, kwargs

    def __init_subclass__(cls, **kwargs):
        """
        初始化子类时设置默认的 instance_type。
        :param kwargs: 包含子类初始化所需的参数。
        """
        super().__init_subclass__()
        cls.__better_type__ = kwargs.get("type", BetterDescriptorInstance)

        # 验证 instance_type 是否为合法类型
        if not issubclass(cls.__better_type__, BetterDescriptorInstance):
            raise TypeError(f"instance_type must be a subclass of BetterDescriptorInstance, got {cls.__better_type__}")

    def __better_get__(self, instance, owner) -> Any:
        """
        获取描述符的值。
        :param instance: 访问描述符的实例。
        :param owner: 描述符所属的类。
        :return: 描述符的值。
        """
        try:
            return self.__better_instance_mapping__[instance].__better_get__(instance, owner, self)
        except KeyError as e:
            raise RuntimeError(f"Instance not found in instance_dict: {e}")

    def __better_set__(self, instance, value):
        """
        设置描述符的值。
        :param instance: 访问描述符的实例。
        :param value: 要设置的值。
        """
        try:
            self.__better_instance_mapping__[instance].__better_set__(instance, value, self)
        except KeyError as e:
            raise RuntimeError(f"Instance not found in instance_dict: {e}")

    def __better_check_existing__(self, instance):
        if instance not in self.__better_instance_mapping__:
            try:
                self.__better_instance_mapping__[instance] = self.__better_new__()
            except Exception as e:
                raise RuntimeError(f"Failed to initialize instance for {instance}: {e}")

    def __better_del__(self, instance):
        """
        删除描述符的值。
        :param instance: 访问描述符的实例。
        """
        try:
            self.__better_instance_mapping__[instance].__better_del__(instance, self)
        except KeyError as e:
            raise RuntimeError(f"Instance not found in instance_dict: {e}")

    def __better_new__(self) -> "BetterDescriptorInstance":
        """
        创建一个新的 BetterDescriptorInstance 实例。
        :return: 新的 BetterDescriptorInstance 实例。
        """
        try:
            ins = self.__better_type__(*self.args, **self.kwargs)
            ins.name = self.name
            return ins
        except Exception as e:
            raise RuntimeError(f"Failed to create instance of type {self.__better_type__}: {e}")

    def __better_init__(self, name, owner):
        ...

    def __get__(self, instance, owner) -> Any:
        """
        实现描述符协议的 __get__ 方法。
        :param instance: 访问描述符的实例。
        :param owner: 描述符所属的类。
        :return: 描述符的值。
        """
        if instance is None:
            return self
        else:
            self.__better_check_existing__(instance)
            return self.__better_get__(instance, owner)

    def __set__(self, instance, value):
        """
        实现描述符协议的 __set__ 方法。
        :param instance: 访问描述符的实例。
        :param value: 要设置的值。
        """
        self.__better_check_existing__(instance)
        self.__better_set__(instance, value)

    def __delete__(self, instance):
        """
        实现描述符协议的 __delete__ 方法。
        :param instance: 访问描述符的实例。
        """
        self.__better_check_existing__(instance)
        self.__better_del__(instance)

    def __set_name__(self, owner, name):
        """
        设置描述符的名称。
        :param owner: 描述符所属的类。
        :param name: 描述符的名称。
        """
        self.__better_init__(name, owner)


class BetterDescriptorInstance:
    name: str = None

    def __better_get__(self, instance, owner, parent) -> Any:
        """
        获取描述符的值（需子类实现）。
        :param instance: 访问描述符的实例。
        :param owner: 描述符所属的类。
        :param parent: 父级描述符。
        :raises NotImplementedError: 如果子类未实现该方法。
        """
        return self

    def __better_set__(self, instance, value, parent):
        """
        设置描述符的值（需子类实现）。
        :param instance: 访问描述符的实例。
        :param value: 要设置的值。
        :param parent: 父级描述符。
        :raises NotImplementedError: 如果子类未实现该方法。
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement __better_set__")

    def __better_del__(self, instance, parent):
        """
        删除描述符的值（需子类实现）。
        :param instance: 访问描述符的实例。
        :param parent: 父级描述符。
        :raises NotImplementedError: 如果子类未实现该方法。
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement __better_del__")

    def __better_init__(self, instance, owner, name):
        """
        初始化描述符(需子类实现)。
        """
