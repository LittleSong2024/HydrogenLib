import pickle
from ..abc import *

class PickleBackend(AbstractBackend):

    def set_model(self, model: 'AbstractModel') -> Self:
        self.model = model
        return self

    def get_model(self) -> 'AbstractModel':
        return self.model

    def save(self, fd):
        pickle.dump(self.model.data, fd)

    def load(self, fd):
        self.model.init(pickle.load(fd))
