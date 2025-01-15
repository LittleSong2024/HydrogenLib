from collections import deque
from typing import Iterable

from . import Tree, HuffmanTree, Graph, BplusTree


class Stack:
    @property
    def ls(self):
        return tuple(self._ls)

    @ls.setter
    def ls(self, ls):
        self._ls = deque(ls)

    def __init__(self, lst: Iterable = None):
        self._ls = deque() if lst is None else deque(lst)

    def push(self, data):
        """
        Push data to stack.
        """
        self._ls.append(data)

    def pop(self):
        """
        Pop data from stack(delete last one).
        if stack is empty, return None.
        """
        return self._ls.pop() if not self.is_empty() else None

    def size(self):
        """
        Get stack size.
        """
        return len(self._ls)

    def is_empty(self):
        """
        Check stack is empty.
        """
        return self.size() == 0

    def top(self):
        """
        Get stack top data.
        """
        return self._ls[-1] if not self.is_empty() else None

    def copy(self):
        """
        Copy stack.
        """
        return self.__class__(self._ls.copy())

    @property
    def at_top(self):
        """
        Same as `.top()`.
        """
        return self.top()

    @at_top.setter
    def at_top(self, data):
        if not self.is_empty():
            self._ls[-1] = data

    def __str__(self):
        return str(self._ls)

    def __iter__(self):
        return iter(self._ls)

    def __getitem__(self, item):
        return self._ls[item]

    def __len__(self):
        return len(self._ls)

    def __setitem__(self, key, value):
        self._ls[key] = value

    def __repr__(self):
        return "Stack({self.lst})".format(self=self)


class Heap:
    def __init__(self, lst=None, reversed=False):
        self.heap = lst or []
        self.iter_reversed = reversed

    def _parent(self, i):
        return (i - 1) // 2

    def _left_child(self, i):
        return 2 * i + 1

    def _right_child(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_down(self, index):
        left = self._left_child(index)
        right = self._right_child(index)
        smallest = index

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _heapify_up(self, index):
        parent = self._parent(index)
        if index > 0 and self.heap[parent] > self.heap[index]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def remove(self, value):
        index = self.heap.index(value)
        self._swap(index, len(self.heap) - 1)
        self.heap.pop()
        self._heapify_down(index)

    def append(self, value):
        self.insert(value)

    def extract_min(self):
        if not self.heap:
            raise IndexError("Heap is empty.")
        min_val = self.heap[0]
        last_val = self.heap.pop()
        if self.heap:
            self.heap[0] = last_val
            self._heapify_down(0)
        return min_val

    def peek(self):
        if not self.heap:
            raise IndexError("Heap is empty.")
        return self.heap[0]

    def copy(self):
        return self.__class__(self.heap.copy())

    def iter(self):
        copy = self.copy()
        while copy:
            yield copy.heap[0]
            last = copy.heap.pop()
            if copy:
                copy.heap[0] = last
                copy._heapify_down(0)

    iter_reversed = False

    def __iter__(self):
        return self.iter() if not self.iter_reversed else reversed(tuple(self.iter()))

    def __len__(self):
        return len(self.heap)
