from collections import deque
from typing import Iterable


class Stack:
    @property
    def stack(self):
        return tuple(self._stack)

    @stack.setter
    def stack(self, stack):
        self._stack = deque(stack)

    def __init__(self, stack: Iterable = None):
        self._stack = deque() if stack is None else deque(stack)

    def push(self, data):
        """
        Push data to stack.
        """
        self._stack.append(data)

    def pop(self):
        """
        Pop data from stack(delete last one).
        if stack is empty, return None.
        """
        return self._stack.pop() if not self.is_empty() else None

    def size(self):
        """
        Get stack size.
        """
        return len(self._stack)

    def is_empty(self):
        """
        Check stack is empty.
        """
        return self.size() == 0

    def peek(self):
        """
        Get stack top data.
        """
        return self._stack[-1] if not self.is_empty() else None

    def copy(self):
        """
        Copy stack.
        """
        return self.__class__(self._stack.copy())

    @property
    def top(self):
        """
        Same as `.top()`.
        """
        return self.peek()

    @top.setter
    def top(self, new):
        if not self.is_empty():
            self._stack[-1] = new

    def __str__(self):
        return str(self._stack)

    def __iter__(self):
        return iter(self._stack)

    def __getitem__(self, item) -> deque:
        return self._stack[item]

    def __len__(self):
        return len(self._stack)

    def __setitem__(self, key, value):
        self._stack[key] = value

    def __repr__(self):
        return "Stack({self.lst})".format(self=self)
