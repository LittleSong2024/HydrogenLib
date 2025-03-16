from __future__ import annotations

import asyncio
import os
import socket
from io import IOBase
from typing import Any, Union

from .._hycore.neostruct import pack_variable_length_int, unpack_variable_length_int_from_readable


class AsyncsocketIO:
    def __init__(self, s: Union[Asyncsocket, Any] = None):
        self._sock = s or Asyncsocket()

    async def write(self, data):
        return await self._sock.sendall(data)

    async def read(self, size: int):
        return await self._sock.recv(size)

    def close(self, closefd=True):
        if not closefd:  # 如果仅仅只是关闭文件描述符，则不关闭socket
            self._sock.close()


class Asyncsocket:
    """
    socket.socket的异步版本
    """
    def __init__(self, s: Union[socket.socket, 'Asyncsocket'] = None, loop: asyncio.AbstractEventLoop = None):
        self.loop = None

        if s is None:
            self.sock = socket.socket()

        elif isinstance(s, Asyncsocket):
            self.sock = s.sock
            self.loop = s.loop
        elif isinstance(s, socket.socket):
            self.sock = s
        else:
            raise TypeError('s must be Asyncsocket, socket.socket or None')

        if self.sock.getblocking():
            self.sock.setblocking(False)  # 异步IO采用非阻塞

        self.loop = self.loop or loop or asyncio.get_running_loop()

    async def sendall(self, data):
        return await self.loop.sock_sendall(
            self.sock, data
        )

    async def recv(self, size: int):
        return await self.loop.sock_recv(
            self.sock, size
        )

    async def recv_into(self, buffer):
        return await self.loop.sock_recv_into(
            self.sock, buffer
        )

    async def accept(self):
        conn, addr = await self.loop.sock_accept(self.sock)
        return Asyncsocket(conn), addr

    async def connect(self, addr, timeout=None):
        if timeout is None:
            return await self.loop.sock_connect(self.sock, addr)
        else:
            return await self.loop.sock_connect(self.sock, addr), timeout

    async def connect_ex(self, addr):
        return self.sock.connect_ex(addr)

    def set_inheriteable(self, inheriteable):
        self.sock.set_inheritable(inheriteable)

    def settimeout(self, timeout=None):
        self.sock.settimeout(timeout)

    def get_inheriteable(self):
        return self.sock.get_inheritable()

    def makefile(self) -> AsyncsocketIO:
        return AsyncsocketIO(self)

    def listen(self, backlog):
        self.sock.listen(backlog)

    def detach(self):
        return self.sock.detach()

    def family(self):
        return self.sock.family

    def fileno(self):
        return self.sock.fileno()

    def getblocking(self):
        return self.sock.getblocking()

    def getpeername(self):
        return self.sock.getpeername()

    def getsockname(self):
        return self.sock.getsockname()

    def getsockopt(self, level, optname, buflen=None):
        try:
            if buflen is None:
                return self.sock.getsockopt(level, optname)
            else:
                return self.sock.getsockopt(level, optname, buflen)
        except OSError:
            return None

    def getsockopt_string(self, level, optname, buflen=None):
        err = self.getsockopt(level, optname, buflen)
        if err:
            return os.strerror(err)

    def gettimeout(self):
        return self.sock.gettimeout()

    def ioctl(self, control, option):
        return self.sock.ioctl(control, option)

    async def bind(self, addr):
        self.sock.bind(addr)

    async def close(self):
        self.sock.close()


class AsyncItemsocket(Asyncsocket):
    async def _recv_item(self):
        io = self.sock.makefile('rb')
        head = unpack_variable_length_int_from_readable(io)
        return io.read(head)

    async def send(self, data):
        length = len(data)
        head = pack_variable_length_int(length)
        return await self.sendall(head + data)

    async def recv(self, size: int):
        for i in range(size):
            yield await self._recv_item()

