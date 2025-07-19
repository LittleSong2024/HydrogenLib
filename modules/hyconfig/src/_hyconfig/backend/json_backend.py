import json
from typing import Self

from ..abc import AbstractBackend, AbstractModel


class JsonBackend(AbstractBackend):

    def set_model(self, model: AbstractModel) -> Self:
        self.model = model
        return self

    def get_model(self) -> 'AbstractModel':
        return self.model

    def save(self, fd):
        json.dump(self.model.data, fd)

    def load(self, fd):
        self.model.init(json.load(fd))
