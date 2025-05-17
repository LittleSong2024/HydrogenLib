from abc import ABC, abstractmethod
from typing import Union, Tuple

protrol_types = {}


class HySocketProtrol(ABC):
    id: Union[str, bytes] = None
    version: Tuple[int, ...] = None

    final_id: bytes = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        global protrol_types

        if not hasattr(cls, "id"):
            raise TypeError("HySocketProtrol subclass must have a 'id' attribute")
        if not hasattr(cls, "version"):
            raise TypeError("HySocketProtrol subclass must have a 'version' attribute")
        if not (cls.id and cls.version):
            raise TypeError("HySocketProtrol subclass must have an valid 'id' and 'version' attribute")

        cls.final_id = cls.id.encode() if isinstance(cls.id, str) else cls.id

        if cls.final_id in protrol_types:
            raise TypeError(f"HySocketProtrol subclass '{cls.__name__}' has a duplicate 'id' attribute")

        protrol_types[cls.final_id] = cls

    @abstractmethod
    def support(self, msg, *args, **kwargs):
        ...

    @abstractmethod
    async def send(self, sock, msg, *args, **kwargs):
        ...

    @abstractmethod
    async def recv(self, sock, *args, **kwargs):
        ...

