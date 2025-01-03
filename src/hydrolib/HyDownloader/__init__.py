import asyncio
import asyncio.queues
import base64
import inspect
import queue
import threading
import time
import urllib.parse
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Union, Coroutine, Callable

import aiofiles
import aiohttp
import requests

from ..path import StringPath
from ..threading_methods import run_new_thread, run_new_daemon_thread


def base64_to_filename(filename):
    return base64.urlsafe_b64decode(filename)


def urlencode_to_filename(filename):
    return urllib.parse.unquote(filename)


def get_size(range_: tuple[int, int]):
    return range_[1] - range_[0] + 1


def get_range_header(start, end):
    return {'Range': f'bytes={start}-{end}'}


def url_to_filename(url):
    filename = urllib.parse.urlparse(url).path.split('/')[-1]
    return urlencode_to_filename(filename)


def can_download(response: Union[aiohttp.ClientResponse, requests.Response]):
    return response.headers['Content-Type'] in ['application/octet-stream', 'application/x-msdownload']


async def get_file_metadata(session: aiohttp.ClientSession, uri):
    async with session.head(uri) as response:
        response.raise_for_status()
        if not can_download(response):
            raise ValueError('Not a binary file')
        return {
            'size': int(response.headers['Content-Length']),
            'filename': url_to_filename(response.url)
        }


def sync_get_file_metadata(uri, timeout=5):
    try:
        response = requests.head(uri, timeout=timeout)
        response.raise_for_status()
        if not can_download(response):
            raise ValueError('Not a binary file')
        url = response.url

        return {
            'size': int(response.headers['Content-Length']),
            'filename': url_to_filename(url)
        }
    except TimeoutError:
        return None


def assign(total, max_chunks, chunk_min_size=1024):
    if chunk_min_size * max_chunks > total:
        ans = []
        pos = 0
        while total:
            if chunk_min_size > total:
                pos += total
                total = 0
            else:
                pos += chunk_min_size
                total -= chunk_min_size

            ans.append((pos, pos + chunk_min_size - 1))
    else:
        chunk_size = total // max_chunks
        ans = [
            (i * chunk_size, (i + 1) * chunk_size - 1) for i in range(max_chunks - 1)
        ]
        ans.append(((max_chunks - 1) * chunk_size, total - 1))

    return ans


debug_lock = threading.Lock()


def debug(*_infomation):
    lineno = inspect.currentframe().f_back.f_lineno
    file = StringPath(inspect.getfile(inspect.currentframe()))
    with debug_lock:
        if len(_infomation) == 1:
            infomation = _infomation[0]
        else:
            # print('\n')
            infomation = '\n'
            for index, info in enumerate(_infomation):
                infomation += '\t' + f'{"<" + str(index) + ">":<5}' + str(info) + '\n'
        # print(f'DEBUG on "{file}:{lineno}", ', end='')
        print(f'[-] "{file.name}:{lineno}", ', end='')
        print(f'from "{threading.current_thread().name}"', end='')
        try:
            task = asyncio.current_task()
            name = task.get_name()
            func_name = task.get_coro().__name__
            print(f', "{name}"({func_name})', end='')
        except RuntimeError:
            pass
        finally:
            print(f' -> {infomation}')


async def process_data(data: asyncio.queues.Queue, target: Union[asyncio.queues.Queue, Callable]):
    type_ = isinstance(target, asyncio.queues.Queue)
    while not data.empty():
        current_data = await data.get()
        debug(f"ProcessData: {repr(current_data[:20]):<20}, into {'func' if type_ else 'queue'}")
        if type_:
            await target.put(current_data)
        else:
            res = target(current_data)
            if isinstance(res, (asyncio.Future, Coroutine)):
                await res


class DownloadCoro:
    def __init__(self, url, range_=None, queue_max_size=0):
        self.chunk_size = 1024 * 1024  # 1MB
        self.url = url
        self.range_ = range_
        self.data = asyncio.queues.Queue(queue_max_size)
        self.size = get_size(self.range_)
        self.pos = 0
        self.task = None

        self.control_event = asyncio.Event()
        self.activate()

    def activate(self):
        self.control_event.set()

    def deactivate(self):
        self.control_event.clear()

    @property
    def start(self):
        return self.range_[0]

    @property
    def end(self):
        return self.range_[1]

    @property
    def completed(self):
        return self.pos >= self.size and not self.hasdata and self.task.done()

    @property
    def hasdata(self):
        return not self.data.empty()

    async def download(self, session: aiohttp.ClientSession):
        if self.completed:
            return
        self.pos = 0
        async with session.get(self.url, headers=get_range_header(*self.range_)) as resp:
            # debug("Get response.")
            while True:
                await self.control_event.wait()
                # debug("Get control event.")
                chunk = await resp.content.read(self.chunk_size)
                # debug("Read chunk... done")
                self.pos += get_size(self.range_)
                # debug("Put data in buffer...")
                await self.data.put(chunk)
                # debug("Put data in buffer... done")
                if self.pos >= self.size:
                    debug("Task end.", f'pos={self.pos}', f'size={self.size}')
                    break

    def start_download(self, session: aiohttp.ClientSession):
        self.task = asyncio.create_task(self.download(session))

    def __str__(self):
        return f'DownloadCoro<completed={self.completed}, pos={self.pos}, range={self.range_}=={self.size}>'

    __repr__ = __str__


# TODO: 保存文件

class DownloadThread:
    def __init__(self, url, range_=None, max_coros=4, queue_max_size=0):
        self.loop = None
        # self.chunk_size = 1024 * 1024  # 1MB
        self.url = url
        self.range = range_
        self.data = asyncio.queues.Queue(queue_max_size)
        self.size = get_size(self.range)
        self.thread = None
        self.session: aiohttp.ClientSession = None
        self.tasks = []  # type: list[DownloadCoro]

        self.assign = assign(self.size, max_coros)
        self.control_event = asyncio.Event()
        self.activate()

    @property
    def start(self):
        return self.range[0]

    @property
    def end(self):
        return self.range[1]

    def activate(self):
        self.control_event.set()

    def deactivate(self):
        self.control_event.clear()

    @property
    def completed(self):
        return not self.thread.is_alive()

    @property
    def hasdata(self):
        return not self.data.empty()

    async def main_coro(self):
        async with self.session:
            for (S, E) in self.assign:
                coro = DownloadCoro(self.url, (S + self.start, E + self.start))
                coro.start_download(self.session)
                self.tasks.append(coro)

            tasks = len(self.tasks)

            async def put_in_data(x):
                await self.data.put((coro, x))

            while True:
                await asyncio.sleep(0)
                await self.control_event.wait()
                done = 0
                for coro in self.tasks:
                    # debug("Current coro: ", coro)
                    await process_data(coro.data, put_in_data)
                    if coro.completed:
                        done += 1
                        continue

                if done == tasks:
                    debug("All task end.")
                    break

    def thread_main(self):
        if self.size == 0:
            return
        self.loop = loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.session = aiohttp.ClientSession(loop=loop)
        try:
            loop.run_until_complete(self.main_coro())
        except Exception as e:
            debug(e)
        finally:
            loop.run_until_complete(self.session.close())
            loop.stop()
            loop.close()

    def start_download(self):
        self.thread = run_new_thread(self.thread_main)

    def wait(self, timeout=None):
        self.thread.join(timeout)

    def __str__(self):
        return f'DownloadThread<completed={self.completed}, size={self.size}>'

    __repr__ = __str__


class DownloadTask:
    def __init__(
            self, uri, root: Union[str, StringPath] = None, file: Union[str, StringPath] = None,
            max_threads=4, thread_max_coros=4,
            thread_buffer_max_size=0, coro_buffer_max_size=0,
            thread_min_chunk_size=0, coro_min_chunk_size=0,
    ):
        self.read_and_write_thread = None
        self.uri = uri

        self.threads = []  # type: list[DownloadThread]

        self.assign = None

        self.max_threads = max_threads
        self.max_coros = thread_max_coros
        self.thread_buffer_max_size = thread_buffer_max_size
        self.coro_buffer_max_size = coro_buffer_max_size
        self.thread_min_chunk_size = thread_min_chunk_size
        self.coro_min_chunk_size = coro_min_chunk_size

        self.metadata = None
        self.root = StringPath(root if root is not None else '.')
        self.file = file

        self.executor: ThreadPoolExecutor = None

        self.control_event = asyncio.Event()
        self.activate()

    def activate(self):
        self.control_event.set()

    def deactivate(self):
        self.control_event.clear()

    @property
    def completed(self):
        return not self.read_and_write_thread.is_alive()

    def __listen_and_write_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__listen_and_write_coro())
        # tasks = asyncio.all_tasks(loop)
        # debug("get", tasks, 'Tasks')
        # asyncio.gather(*tasks)
        # loop.run_until_complete(loop.shutdown_asyncgens())
        debug("Close event loop.")
        loop.close()
        self.executor.shutdown(wait=True)

    async def __listen_and_write_coro(self):  # TODO: 修复文件写入时没有写全的问题
        self.executor = ThreadPoolExecutor()
        total = 0
        async with aiofiles.open(self.root.using(self.file), 'wb', executor=self.executor) as fd:
            debug("Get fd", fd.name)
            while True:
                done = 0
                # await asyncio.sleep(0)
                await self.control_event.wait()
                for thread in self.threads:
                    if thread.completed and not thread.hasdata:
                        debug("Completed thread:", thread)
                        done += 1
                        continue

                    coro: DownloadCoro
                    chunk: bytes
                    while not thread.data.empty():
                        coro, chunk = await thread.data.get()
                        await fd.seek(coro.start + coro.pos)
                        await fd.write(chunk)
                        length = len(chunk)
                        debug(f"Write {length} bytes", f'from {coro}')
                        total += length
                await fd.flush()

                if done == len(self.threads):
                    debug("All thread end.", (len(self.threads), done))
                    break
        # await fd.flush()
        # debug('Flush end')
        # debug("Close", fd.closed)
        debug(total)
        debug("Read write thread end.")
        return await asyncio.sleep(0)

    def start_download(self):
        self.metadata = sync_get_file_metadata(self.uri)
        if self.file is None:
            self.file = self.metadata['filename']
        if self.metadata is None:
            raise ConnectionError('Cannot get metadata')
        self.size = self.metadata['size']
        self.assign = assign(self.metadata['size'], self.max_threads, self.thread_min_chunk_size)
        debug("Get meta", self.metadata)
        debug(self.assign)

        for (S, E) in self.assign:
            thread = DownloadThread(self.uri, (S, E), self.max_coros, self.thread_buffer_max_size)
            thread.start_download()
            self.threads.append(thread)

        self.read_and_write_thread = run_new_thread(self.__listen_and_write_thread)

    def wait(self, timeout=None):
        for thread in self.threads:
            thread.wait(timeout)


class DownloadManager:

    def __init__(self, max_tasks=4, max_threads=4, max_coros=16, thread_buffer_max_size=0, coro_buffer_max_size=0):
        self.max_tasks = max_tasks
        self.max_threads = max_threads
        self.max_coros = max_coros
        self.thread_buffer_max_size = thread_buffer_max_size
        self.coro_buffer_max_size = coro_buffer_max_size

        self.tasks = []  # type: list[DownloadTask]
        self.n = 0

        self.tasks_lock = threading.Lock()

        self.complete_tasks = queue.Queue()

        self.check_interval = 0.1
        self.thread = None

        self.__start_checker()

    def __start_checker(self):
        self.thread = run_new_daemon_thread(self.__check_download_thread)

    def new_task(self, uri, root=None, file=None) -> DownloadTask:
        """
        创建一个新的下载任务
        """
        return DownloadTask(
            uri, root, file,
            self.max_threads, self.max_coros, thread_buffer_max_size=self.thread_buffer_max_size,
            coro_buffer_max_size=self.coro_buffer_max_size
        )

    def submit_task(self, task: 'DownloadTask'):
        with self.tasks_lock:
            if self.n >= self.max_tasks:
                raise RuntimeError('too many tasks')
            self.tasks.append(task)
            self.n += 1
            task.start_download()

    def wait_task(self, task: 'DownloadTask'):
        task.wait()

    def wait_all(self):
        for task in self.tasks:
            task.wait()

    def __check_download_thread(self):
        while True:
            # time.sleep(0.1)
            time.sleep(self.check_interval)
            for i, task in enumerate(self.tasks):
                if task.read_and_write_thread is None:
                    continue  # 任务未开始
                if task.completed:
                    with self.tasks_lock:
                        self.tasks.pop(i)
                        self.n -= 1
                        self.complete_tasks.put(task)
