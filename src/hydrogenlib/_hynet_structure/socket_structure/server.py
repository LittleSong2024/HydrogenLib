import asyncio
from ..._hycore.async_socket import Asyncsocket


class Server:
    def __init__(self, port: int, loop: asyncio.AbstractEventLoop = None):
        self._port = port
        self._loop = loop or asyncio.get_running_loop()
        self._running = False

    @property
    def port(self):
        return self._port

    @property
    def loop(self):
        return self._loop

    def start(self):
        self._running = True
        self.loop.create_task(self.run())

    def stop(self):
        self._running = False
        self._loop.call_soon_threadsafe(self._loop.stop)

    async def run(self):
        server = Asyncsocket()
        while self._running:
            conn, addr = await server.accept()
            self.loop.create_task(self.handle(conn, addr))

    def exec(self):
        return self.loop.run_forever()

    async def handle(self, conn: Asyncsocket, addr):
        ...
