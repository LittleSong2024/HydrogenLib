import asyncio
from typing import AsyncGenerator

from ..._hycore.async_socket import Asyncsocket
from ..._hycore.neostruct import pack_variable_length_int, unpack_variable_length_int


async def sock_to_iterable(s: Asyncsocket):
    while True:
        yield await s.recv(1)


def sync_iter(agr: AsyncGenerator):
    loop = asyncio.get_running_loop()
    try:
        while True:
            yield loop.run_until_complete(agr.__anext__())
    except (StopAsyncIteration, asyncio.CancelledError, GeneratorExit):
        loop.run_until_complete(agr.aclose())


def get_part_from_sock(s: Asyncsocket):
    sock_generator = sync_iter(sock_to_iterable(s))
    data, _ = unpack_variable_length_int(
        sock_generator
    )
    sock_generator.close()
    return data


async def build_part_into_sock(data: bytes, s: Asyncsocket):
    length = len(data)
    await s.sendall(
        pack_variable_length_int(length) + data
    )
