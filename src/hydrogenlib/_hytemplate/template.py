from .abstract import AbstractMarker
from .._hycore.data_structures import Stack
from .._hycore.utils import GettingPath


class ItemGettingPath(GettingPath):
    def getnext(self, current, next):
        return current[next]

    def setnext(self, current, next, value):
        current[next] = value


class Template:
    def __init__(self, template):
        self._template = template
        self._marker_paths = list(map(ItemGettingPath, self._scan_markers()))  # type: list[ItemGettingPath]

    def _scan_markers(self, current=None, stack=None):
        if current is None:
            current = self._template
            stack = Stack()

        if isinstance(current, dict):
            for key, value in current.items():
                stack.push(key)  # 记录当前键
                if isinstance(value, AbstractMarker):
                    yield stack.copy()  # 返回当前路径
                else:
                    yield from self._scan_markers(value, stack)  # 递归处理子节点
                stack.pop()  # 回溯

    def fill_value(self, **kwargs):
        template = self._template.copy()
        for path in self._marker_paths:
            parent_dict = path.parent.touch(template)
            parent_dict[path.name] = parent_dict[path.name].generate(self, **kwargs)
        return template
