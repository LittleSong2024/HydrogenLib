class _Empty:
    ...


class EventBase:
    def __init__(self):
        self.__accepted = False

    def accept(self):
        self.__accepted = True

    def deaccept(self):
        self.__accepted = False


class SetEvent(EventBase):
    def __init__(self, old, new):
        super().__init__()
        self.old = old
        self.new = new


class DeleteEvent(EventBase):
    def __init__(self, key_obj, value):
        super().__init__()
        self.key = key_obj
        self.value = value


class GetEvent(EventBase):
    def __init__(self, key_obj, value):
        super().__init__()
        self.key = key_obj
        self.result = value

    def set_result(self, value):
        self.result = value
