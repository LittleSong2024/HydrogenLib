import asyncio
import socket
from typing import Any, Union

from .._hycore.neostruct import pack_variable_length_int, unpack_variable_length_int_from_readable


class Asyncsocket:
    """
    socket.socket的异步版本
    """
    def __init__(self, s: Union[socket.socket, Any] = None, loop: asyncio.AbstractEventLoop = None):
        if s is None:
            self.sock = socket.socket()
        elif isinstance(s, self.__class__):
            self.sock = s.sock
        else:
            self.sock = s

        if self.sock.getblocking() is True:
            self.sock.setblocking(False)  # 异步IO采用非阻塞

        self.loop = loop if loop else asyncio.get_running_loop()

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

    def settimeout(self, timeout=None):
        self.sock.settimeout(timeout)

    def listen(self, backlog):
        self.sock.listen(backlog)

    def detach(self):
        return self.sock.detach()

    def family(self):
        return self.sock.family

    def fileno(self):
        return self.sock.fileno()

    def get_inheriteable(self):
        return self.sock.get_inheritable()

    def getblocking(self):
        return self.sock.getblocking()

    def getpeername(self):
        return self.sock.getpeername()

    def getsockname(self):
        return self.sock.getsockname()

    def getsockopt(self, level, optname, buflen=None):
        if buflen is None:
            return self.sock.getsockopt(level, optname)
        else:
            return self.sock.getsockopt(level, optname, buflen)

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

