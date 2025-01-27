from typing import final

from .items import ConfigItem
from ..abc.backend import BackendABC


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
        # 这将引发TypeError,您应该保证default和type的允许类型是一样的
        configItem3 = ConfigItem('configItem3-key', type=ListType, default=[])
        # 您可以随意指定配置项的键,这个键作为配置文件中显示的键
        # ConfigContainer会自动完成key_to_attr的转换,只要你使用__getitem__和__setitem__方法,注意,这些方法的转换是以属性名作为最高的优先转换
        configItem4 = ConfigItem('configItem3', ...)
        # 当您使用 container['ConfigItem3'] 动态访问ConfigItem3时,实际返回的还是ConfigItem3,因为属性和键的判断是属性优先
    ```
    """
    _instance = None

    @final
    def __new__(cls, *args, **kwargs):
        if cls.backend is None:
            raise NotImplementedError("必须实现backend属性")
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    backend: BackendABC = None

    def __init__(self, file):
        self.backend.set_file(file)

        self._config_attrs: set = None
        self.changes: set = set()

        self._config_key_to_attr_mapping = {}
        self._config_attr_to_key_mapping = {}

        self.__get_keys(self)
        self.__build_mapping()
        self.__load()

    @classmethod
    def __get_keys(cls, self: 'ConfigContainer'):
        ls = set()
        for attr in dir(cls):
            if attr.startswith('__'):
                continue
            value = getattr(cls, attr)
            if isinstance(value, ConfigItem):
                ls.add(attr)
        self._config_attrs = ls

    def __load(self):
        self.backend.load()
        for key, value in self.backend.items():
            setattr(self, self.__map_to_attr(key), value)
        self.changes.clear()

    def __build_mapping(self):
        for attr in self.config_names():
            key = self.__get_item(attr).key
            self._config_key_to_attr_mapping[key] = attr
            self._config_attr_to_key_mapping[attr] = key

    @classmethod
    def __get_item(cls, item_attr) -> ConfigItem:
        return getattr(cls, item_attr)

    def __map_to_attr(self, key):
        return self._config_key_to_attr_mapping[key]

    def __map_to_key(self, attr):
        return self._config_attr_to_key_mapping[attr]

    def __auto_map_to_key(self, key_or_attr, prefer_attr=False):
        if not prefer_attr and key_or_attr in self._config_attr_to_key_mapping:
            return key_or_attr
        elif key_or_attr in self.config_names():
            return self.__map_to_key(key_or_attr)
        else:
            raise KeyError(f'{key_or_attr} is not a valid config item or key')

    def __auto_map_to_attr(self, key_or_attr, prefer_key=False):
        if not prefer_key and key_or_attr in self.config_names():
            return key_or_attr
        elif key_or_attr in self._config_key_to_attr_mapping:
            return self.__map_to_attr(key_or_attr)
        else:
            raise KeyError(f'{key_or_attr} is not a valid config item or key')

    def __save(self, keys_or_attrs):
        for name in keys_or_attrs:
            attr = self.__auto_map_to_attr(name)
            value = self[attr]
            self.backend.set(name, value)

        self.backend.save()

    @property
    def is_first_loading(self):
        """
        是否是第一次加载
        """
        return self.backend.is_first_loading

    def config_names(self):
        """
        返回作为配置项的属性名集合
        """
        return self._config_attrs

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

    def __getitem__(self, key):
        attr = self.__auto_map_to_attr(key)
        if attr in self.config_names():
            return getattr(self, attr)
        else:
            raise KeyError(f'{key} is not a config item or key')

    def __setitem__(self, key, value):
        attr = self.__auto_map_to_attr(key)
        if attr in self.config_names():
            setattr(self, attr, value)
        else:
            raise KeyError(f'{key} is not a config item or key')

    def save(self):
        """
        保存配置(仅限所有改动)
        """
        self.__save(self.changes)

    def save_all(self):
        """
        保存所有配置
        """
        self.__save(self.config_names())

    def on_change(self, key):
        self.changes.add(key)
