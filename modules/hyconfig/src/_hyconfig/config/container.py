from _hyconfig.config.manager import BackendManager, ModelManager


class ConfigError(Exception):
    ...


class HyConfig:
    """
    配置主类
    通过继承并添加ConfigItem类属性来定义配置结构
    """
    backends = ...
    models = ...

    def __init__(self):
        self.models = ModelManager()
        self.backends = BackendManager()

