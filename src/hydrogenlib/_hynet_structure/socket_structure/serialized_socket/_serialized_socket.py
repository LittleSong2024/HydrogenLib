import asyncio
import socket
from typing import *

from .._methods import get_part_from_sock, build_part_into_sock
from ...._hycore.async_socket import Asyncsocket
from ....hystruct.Serializers import Serializer, dumps, loads


class serialized_socket:
    def __init__(self, s: Union[socket.socket, Any] = None, loop: asyncio.AbstractEventLoop = None,
                 serializer: Serializer = dumps):
        self.loop = loop if loop else asyncio.get_running_loop()
        self.serializer = serializer
        self.s = Asyncsocket(s)
        self._forever_stop = False

    async def connect(self, addr, port, timeout=None):
        await self.s.connect((addr, port), timeout)

    async def send(self, data):
        bytes_data = dumps(data, serializer=self.serializer)
        await build_part_into_sock(bytes_data, self.s)

    async def send_iter(self, items):
        for item in items:
            await self.send(item)

    async def send_aiter(self, items):
        async for item in items:
            await self.send(item)

    async def recv(self):
        bytes_data = await get_part_from_sock(self.s)
        return loads(bytes_data)

    async def recv_iter(self, size=1):
        for i in range(size):
            yield await self.recv()

    async def recv_forever(self):
        while not self._forever_stop:
            yield await self.recv()

    async def close(self):
        self._forever_stop = True
        await self.s.close()
