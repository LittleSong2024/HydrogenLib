from .._hycore.async_socket import Asyncsocket
from .._hycore.data_structures import Stack

from .methods import *


def pack__connect_length(data):
    return pack_variable_length_int(len(data)) + data

def unpack__connect_length(data):
    length, count = unpack_variable_length_int(data)
    return length


class HySocket:
    def __init__(self, sock=None, default_protrols: list[HySocketProtrol] = None):
        self._sock = Asyncsocket(sock)
        self._stack = Stack()
        self.default_protrols = default_protrols or []

    def _get_supported_protrol(self, protrol, msg, *args, **kwargs):
        if protrol and protrol.support(*args, **kwargs):
            return protrol
        for i in self.default_protrols:
            if i.support(*args, **kwargs):
                return i

        raise ValueError('No protrol support this msg')

    async def sendall(self, data):
        """
        以原始模式发送数据
        """
        # self._stack.top += len(data)  # 更新数据长度
        await self._sock.sendall()

    async def send_protrol(self, msg, protrol: HySocketProtrol = None, *args, **kwargs):
        """
        以协议模式发送数据
        """
        # self._stack.push(0)  # 追踪发送长度

        protrol = self._get_supported_protrol(protrol, msg, *args, **kwargs)
        head = build_protrol_head(protrol)

        await self._sock.sendall(b'[' + head + b']')
        await protrol.send(self, msg, *args, **kwargs)

        # length = self._stack.pop()
        # await self._sock.sendall(build_protrol_tail(protrol, length))





