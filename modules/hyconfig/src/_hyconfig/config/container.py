from typing import Type

from _hycore.utils import DoubleDict
from .items import ConfigItem, ConfigItemInstance
from .types import ConfigTypeMapping, builtin_type_mapping
from ..abc.backend import AbstractBackend


def get_keys_by_type(dct, tp):
    ls = set()
    for attr in dct:
        if attr.startswith('__'):
            continue
        value = dct[attr]
        if isinstance(value, tp):
            ls.add(attr)
    return ls


def get_attrs_by_type(obj, tp):
    ls = set()
    for attr in dir(obj):
        if attr.startswith('__'):
            continue
        value = getattr(obj, attr)
        if isinstance(value, tp):
            ls.add(attr)
    return ls


class ConfigError(Exception):
    ...


class PreConfigCheckError(ConfigError):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        return f"Failed to create config container ==> {self.e}"


def _build_items(cls: 'Type[HyConfig]'):
    cls.__cfgitems__ = get_attrs_by_type(cls, ConfigItem)


def _build_mapping(cls: 'Type[HyConfig]'):
    mapping = cls.__cfgmapping__
    items = cls.__cfgitems__

    for name in items:
        item = getattr(cls, name)  # type: ConfigItem
        key = item.key

        if key is None:
            item.key = key = name

        if name in mapping:  # 有配置项的name与其他配置项的key或name冲突
            raise PreConfigCheckError(f'{name} is a config item and key conflict')
        if key in mapping:  # 有配置项的key与其他配置项的key或name冲突
            raise PreConfigCheckError(f'{key} is a config item and key conflict')

        item.attr = name

        mapping[key] = name  # 保存映射关系


class HyConfig:
    """
    配置主类
    通过继承并添加ConfigItem类属性来定义配置结构

    比如:
    ```
    class MyConfig(ConfigContainer):
        configItem1 = ConfigItem('configItem1', type=IntType, default=0)
        configItem2 = ConfigItem('configItem2', type=BoolType, default=True)

        # configItemError1 = ConfigItem('configItemError1', type=IntType, default='123')
        #   这将引发TypeError,您应该保证default和type的允许类型是一样的

        configItem3 = ConfigItem('configItem3-key', type=ListType, default=[])
        #   您可以随意指定配置项的键,这个键作为配置文件中显示的键

        # ConfigContainer会自动完成key_to_attr的转换,只要你使用__getitem__和__setitem__方法,注意,这些方法的会将属性名作为转换标准

        # configItem4 = ConfigItem('configItem3', ...)  # Error
        #   您无法将一个配置项的key设置成已存在的配置项的名称或键,这将会在定义时报错: configItem3 is a config item and key conflict
    ```
    除了类型不匹配错误会抛出 TypeError ,此外所有错误均继承于 ConfigError
    """

    # 内部属性
    __cfgitems__: set = None
    __cfgmapping__: DoubleDict = None

    # 可重写配置属性
    __cfgtypemapping__: ConfigTypeMapping = builtin_type_mapping
    __cfgautoload__ = False
    __cfgfile__ = None
    __cfgbackend__: AbstractBackend = None

    @property
    def cfg_items(self):
        return self.__cfgitems__

    @property
    def cfg_file(self):
        return self.__cfgfile__

    @property
    def cfg_backend(self):
        return self.__cfgbackend__

    @property
    def cfg_mapping(self):
        return self.__cfgmapping__

    @property
    def cfg_autoload(self):
        return self.__cfgautoload__

    @property
    def cfg_model(self):
        return self.__cfgbackend__.get_model()

    @classmethod
    def get_cfgitem(cls, name, instance) -> 'ConfigItemInstance':
        return getattr(cls, name).get_instance(instance)

    def __init_subclass__(cls, **kwargs):  # 对于每一个子类,都会执行一次映射构建
        cls.__cfgitems__ = cls.__cfgitems__ or set()
        cls.__cfgmapping__ = DoubleDict()

        cls.__cfgautoload__ = kwargs.get('autoload', cls.__cfgautoload__)

        _build_items(cls)
        _build_mapping(cls)

    def __init__(self):
        self.changes: set = set()

        if self.cfg_autoload:
            self.load(self.cfg_file)

    def load(self, file=None):
        file = file or self.cfg_file
        self.cfg_backend.load(file)

    def validate(self, key_or_attr, value, error=False):
        if not self.exists(key_or_attr):
            raise KeyError(f'{key_or_attr} is not a valid config item or key')
        return self.get_cfgitem(key_or_attr, self).validate(value, error)

    def exists(self, key_or_attr):
        """
        判断配置项是否存在
        """
        attr = self.as_attrname(key_or_attr)
        return attr in self.keys()

    def keys(self):
        """
        返回作为配置项的属性名集合
        """
        return self.cfg_items

    def values(self):
        """
        返回作为配置项的属性值集合
        """
        return [getattr(self, key) for key in self.keys()]

    def items(self):
        """
        返回作为配置项的属性名和属性值集合
        """
        return [(key, getattr(self, key)) for key in self.keys()]

    def clear(self):
        for attr in self.keys():
            data = self.get_cfgitem(attr, self)
            setattr(self, attr, data.default)

    def as_attrname(self, key_or_attr):
        if key_or_attr in self.cfg_items:
            return key_or_attr
        elif key_or_attr in self.cfg_mapping:
            return self.cfg_mapping[key_or_attr]
        else:
            raise KeyError(f'{key_or_attr} is not a valid config item or key')

    def __getitem__(self, key):
        attr = self.as_attrname(key)
        if attr in self.keys():
            return getattr(self, attr)
        else:
            raise KeyError(f'{key} is not a config item or key')

    def __setitem__(self, key, value):
        attr = self.as_attrname(key)
        if attr in self.keys():
            setattr(self, attr, value)
        else:
            raise KeyError(f'{key} is not a config item or key')
