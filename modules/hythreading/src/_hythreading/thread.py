from threading import Thread as _Thread


class HyThread(_Thread):
    def __init__(self, target=None, args=None, kwargs=None):
        super().__init__()
        self._target, self._args, self._kwargs = target, args, kwargs

    def on_start(self):
        ...

    def on_exit(self):
        ...

    def run(self):
        self.on_start()
        self._target(*self._args, **self._kwargs)
        self.on_exit()
