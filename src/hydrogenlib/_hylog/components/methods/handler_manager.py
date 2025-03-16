class HandlerManager:
    def __init__(self, handlers=None):
        self.handlers = handlers or []

    def add_handlers(self, *handlers):
        self.handlers.extend(handlers)

    def remove_handlers(self, *handlers):
        for handler in handlers:
            self.handlers.remove(handler)

    def call(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.call(*args, **kwargs)
