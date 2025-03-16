from .. protrol_abc import HySocketProtrol


class OriginProtrol(HySocketProtrol):
    id = b'origin'

    def support(self, msg, *args, **kwargs):
        return isinstance(msg, bytes)

    async def send(self, sock, msg, *args, **kwargs):
        await sock.sendall(msg)

    async def recv(self, sock, *args, **kwargs):
        pass
