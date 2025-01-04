from time import sleep, time


class Clock:
    def __init__(self):
        self.last_time = None

    def strike(self, interval):
        """
        确保任务以指定的间隔时间执行。
        :param interval: 刷新间隔时间，单位为秒
        """
        if self.last_time is None:
            self.last_time = time()

        current_time = time()
        elapsed_time = current_time - self.last_time
        if elapsed_time >= interval:
            sleep(interval)
        else:
            sleep(interval - elapsed_time)
        self.last_time = time()
