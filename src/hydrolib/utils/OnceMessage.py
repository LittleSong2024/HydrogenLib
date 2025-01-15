import time


class OnceMessage:
    def __init__(self):
        self.message = None
        self.is_sent = False

    def set(self, message):
        self.message = message
        self.is_sent = True

    def get(self, timeout=None):
        start_time = time.time()
        if timeout is None:
            timeout = float('inf')
        while True:
            time.sleep(0.01)
            if self.is_sent:
                return self.message
            if time.time() - start_time > timeout:
                raise TimeoutError()
