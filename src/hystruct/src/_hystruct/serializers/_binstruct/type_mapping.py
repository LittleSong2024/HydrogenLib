from ...._hycore.data_structures import HuffmanTree
from ...._hycore.type_func import get_qualname


class TypeMapping:
    def __init__(self, type_list):
        self.list = type_list
        self.tree = None  # type: HuffmanTree

    def append(self, type):
        self.list.append(get_qualname(type))

    def remove(self, type):
        self.list.remove(get_qualname(type))

    def exists(self, type):
        return get_qualname(type) in self.list

    def build_tree(self):
        self.tree = HuffmanTree.from_list(map(get_qualname, self.list))

    def to_bytes(self, type):
        return self.tree.to_bytes(get_qualname(type))
