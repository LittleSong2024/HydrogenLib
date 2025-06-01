from abc import ABC, abstractmethod


class TTLCacheBackend(ABC):
    @abstractmethod
    def get(self, key):
        """
        Get a value from the cache.
        :param key: The key to get.
        :return:
        """

    @abstractmethod
    def set(self, key, value, ttl=None):
        """
        set a key-value pair in the cache.
        :param key: The key to set.
        :param value: The value to set.
        :param ttl: The time to live for the key(Unit: second).
        :return: Depends on the cache backend.
        """

    @abstractmethod
    def delete(self, key): ...

    @abstractmethod
    def clear(self): ...

    def keys(self):
        """
        Get all keys in the cache. Not every cache backend supports this.
        :return: None | Iterable
        """

    def ttl(self, key, ttl=None, unit='s'): ...
