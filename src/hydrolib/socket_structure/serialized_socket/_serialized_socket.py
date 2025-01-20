import asyncio
from .._methods import get_part_from_sock, build_part_into_sock
from ...hystruct.Serializers import Serializer, dumps, loads
from ...socket import Asyncsocket
from typing import *

import socket


class serialized_socket:
    def __init__(self, s: Union[socket.socket, Any] = None, loop: asyncio.AbstractEventLoop = None, serializer: Serializer = dumps):
        self.loop = loop if loop else asyncio.get_running_loop()
        self.serializer = serializer
        self.s = Asyncsocket(s)

    async def connect(self, addr, port, timeout=None):
        await self.s.connect((addr, port))

    async def send(self, data):
        bytes_data = dumps(data, serializer=self.serializer)
        await build_part_into_sock(bytes_data, self.s)

    async def recv(self, size):
        bytes_data = await get_part_from_sock(self.s)
        return loads(bytes_data)

