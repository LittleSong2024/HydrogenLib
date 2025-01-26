from .items import ConfigItem, ConfigItemInstance
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
        # 注意: ConfigItem的位置参数1(key)应与类属性名称相同
    ```
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    backend: BackendABC = None

    def __init__(self, file):
        self._file = file

        self.changes = set()

        self.backend.set_file(file)
        self.__load()

    def __load(self):
        self.backend.load()
        for key, value in self.backend.items():
            setattr(self, key, value)
        self.changes.clear()

    def changeEvent(self, key):
        self.changes.add(key)

    @property
    def is_first_loading(self):
        """
        是否是第一次加载
        """
        return self.backend.is_first_loading

    @classmethod
    def keys(cls):
        ls = set()
        for attr in dir(cls):
            if attr.startswith('__'):
                continue
            value = getattr(cls, attr)
            if isinstance(value, ConfigItem):
                ls.add(attr)
        return ls

    def values(self):
        return [getattr(self, key) for key in self.keys()]

    def items(self):
        return [(key, getattr(self, key)) for key in self.keys()]

    def save(self):
        for key in self.changes:
            value = getattr(self, key)
            self.backend.set(key, value)

        self.backend.save()
