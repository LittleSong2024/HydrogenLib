from pathlib import Path
from typing import Union

from .const import *
from .items import ConfigItem, ConfigData
from ..abc.backend import BackendABC
from ..._hycore.utils import DoubleDict


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


class NewConfigContainerError(ConfigError):
    def __init__(self, e):
        self.e = e

    def __str__(self):
        return f"Failed to create config container ==> {self.e}"


def _build_items(self: 'type[ConfigContainer]'):
    self.__cfgitems__ = get_attrs_by_type(self, ConfigItem)


def _build_mapping(self: 'type[ConfigContainer]'):
    mapping = self.__cfgmapping__
    items = self.__cfgitems__

    for name in items:
        item = getattr(self, name)  # type: ConfigItem
        key = item.key

        if item.key == AUTO:
            item.key = key = name

        if name in mapping:  # 有配置项的name与其他配置项的key或name冲突
            raise NewConfigContainerError(f'{name} is a config item and key conflict')
        if key in mapping:  # 有配置项的key与其他配置项的key或name冲突
            raise NewConfigContainerError(f'{key} is a config item and key conflict')

        item.attr = name

        mapping[key] = name  # 保存映射关系


class ConfigContainer:
    """
    配置主类
    继承并添加ConfigItem类属性
    所有ConfigContainer是通用的
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
    """

    __cfgitems__: set = None
    __cfgmapping__: DoubleDict = None
    __cfgbackend__: BackendABC = None
    __cfgfile__: Union[Path, str] = None

    __cfgautoload__ = False

    @property
    def cfg_items(self):
        return self.__cfgitems__

    @property
    def cfg_backend(self):
        return self.__cfgbackend__

    @property
    def cfg_mapping(self):
        return self.__cfgmapping__

    @property
    def cfg_file(self):
        return self.__cfgfile__

    @property
    def cfg_autoload(self):
        return self.__cfgautoload__

    @classmethod
    def get_cfgitem(cls, name, instance) -> 'ConfigData':
        return getattr(cls, name).from_instance(instance)

    def __init_subclass__(cls, **kwargs):  # 对于每一个子类,都会执行一次映射构建
        cls.__cfgitems__ = cls.__cfgitems__ or set()
        cls.__cfgmapping__ = DoubleDict()

        _build_items(cls)
        _build_mapping(cls)

    def __init__(self):
        self.changes: set = set()

        if self.cfg_autoload:
            self.load(self.cfg_file)

    def load(self, file=None):
        self.cfg_backend.set_file(file)
        self._load()

    def validate(self, key_or_attr, value, error=False):
        if not self.exists(key_or_attr):
            raise KeyError(f'{key_or_attr} is not a valid config item or key')
        item = self.get_cfgitem(key_or_attr, self)
        if error:
            item.tm_validate(value)
            return True
        else:
            return item.tp_validate(value)

    @property
    def existing(self):
        """
        加载时配置文件是否存在
        """
        return not self.__cfgbackend__.existing

    def exists(self, key_or_attr):
        """
        判断配置项是否存在
        """
        attr = self.to_attr(key_or_attr)
        return attr in self.config_names()

    def config_names(self):
        """
        返回作为配置项的属性名集合
        """
        return self.cfg_items

    def config_values(self):
        """
        返回作为配置项的属性值集合
        """
        return [getattr(self, key) for key in self.config_names()]

    def config_items(self):
        """
        返回作为配置项的属性名和属性值集合
        """
        return [(key, getattr(self, key)) for key in self.config_names()]

    def save(self):
        """
        保存配置(仅限所有改动)
        """
        self._save(self.changes)

    def save_all(self):
        """
        保存所有配置
        """
        self._save(self.config_names())

    def clear_changes(self):
        self.changes.clear()

    def reset(self):
        for attr in self.config_names():
            data = self.get_cfgitem(attr, self)
            setattr(self, attr, data.default)

    def to_attr(self, key_or_attr):
        if key_or_attr in self.cfg_items:
            return key_or_attr
        elif key_or_attr in self.cfg_mapping:
            return self.cfg_mapping[key_or_attr]
        else:
            raise KeyError(f'{key_or_attr} is not a valid config item or key')

    def on_change(self, key, old, new):
        self.changes.add(key)

    def _load(self):
        self.cfg_backend.load()
        for key, value in self.cfg_backend.items():
            attr = self.to_attr(key)
            data = self.get_cfgitem(attr, self)

            if data.tp_validate(value):
                setattr(self, attr, value)
            else:
                setattr(self, attr, data.default)

        self.changes.clear()

    def __getitem__(self, key):
        attr = self.to_attr(key)
        if attr in self.config_names():
            return getattr(self, attr)
        else:
            raise KeyError(f'{key} is not a config item or key')

    def __setitem__(self, key, value):
        attr = self.to_attr(key)
        if attr in self.config_names():
            setattr(self, attr, value)
        else:
            raise KeyError(f'{key} is not a config item or key')

    @classmethod
    def _get_item(cls, item_attr) -> ConfigItem:
        return getattr(cls, item_attr)

    def _save(self, keys_or_attrs):
        for name in keys_or_attrs:
            attr = self.to_attr(name)
            value = self.get_cfgitem(name, self)
            self.cfg_backend.set(name, value.tp_transform())

        self.cfg_backend.save()

