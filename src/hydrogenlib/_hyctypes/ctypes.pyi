from __future__ import annotations

from typing import Protocol, runtime_checkable, overload, Callable


@runtime_checkable
class CData(Protocol):
    """
    This non-public class is the common base class of all ctypes data types. Among other things, all ctypes type
    instances contain a memory block that hold C compatible data; the address of the memory block is returned by the
    addressof() helper function. Another instance variable is exposed as _objects; this contains other Python objects
    that need to be kept alive in case the memory block contains pointers.


    Attributes:
        - _b_base: Sometimes ctypes data instances do not own the memory block they contain, instead they
            share part of the memory block of a base object. The _b_base_ read-only member is the root ctypes object that
            owns the memory block.

        - _b_needsfree: This read-only member is True if the memory block is owned by the ctypes
            object, False otherwise.

        - _objects: This member is either None or a dictionary containing Python objects that
            need to be kept alive so that the memory block contents is kept valid. This object is only exposed for debugging;
            never modify the contents of this dictionary.

    """

    def __init__(self, *args, **kwargs):
        ...

    @classmethod
    def from_buffer(cls, source, offset):
        """
        This method returns a ctypes instance that shares the buffer of the source object. The source object must
        support the writeable buffer interface. The optional offset parameter specifies an offset into the source
        buffer in bytes; the default is zero. If the source buffer is not large enough a ValueError is raised.

        Raises an auditing event ctypes.cdata/buffer with arguments pointer, size, offset.
        """

    @classmethod
    def from_buffer_copy(cls, source, offset):
        """
        This method creates a ctypes instance, copying the buffer from the source object buffer which must be
        readable. The optional offset parameter specifies an offset into the source buffer in bytes; the default is
        zero. If the source buffer is not large enough a ValueError is raised.

        Raises an auditing event ctypes.cdata/buffer with arguments pointer, size, offset.
        """

    @classmethod
    def from_address(cls, address):
        """
        This method returns a ctypes type instance using the memory specified by address which must be an integer.

        This method, and others that indirectly call this method, raises an auditing event ctypes.cdata with argument
        address.
        """

    @classmethod
    def from_param(cls, obj):
        """
        This method adapts obj to a ctypes type. It is called with the actual object used in a foreign function call
        when the type is present in the foreign function’s argtypes tuple; it must return an object that can be used
        as a function call parameter.

        All ctypes data types have a default implementation of this classmethod that normally returns obj if that is an
        instance of the type. Some types accept other objects as well.
        """

    @classmethod
    def in_dll(cls, library, name):
        """
        This method returns a ctypes type instance exported by a shared library. name is the name of the symbol that
        exports the data, library is the loaded shared library.
        """

    _b_base: CData
    _b_needsfree: bool
    _objects: dict | None


class SimpleCData(CData):
    """
    This non-public class is the base class of all fundamental ctypes data types. It is mentioned here because it
    contains the common attributes of the fundamental ctypes data types. _SimpleCData is a subclass of _CData,
    so it inherits their methods and attributes. ctypes data types that are not and do not contain pointers can now
    be pickled.

    Attributes:
        - value:
            This attribute contains the actual value of the instance. For integer and pointer types,
            it is an integer, for character types, it is a single character bytes object or string, for character pointer
            types it is a Python bytes object or string.

            When the value attribute is retrieved from a ctypes instance, usually a new object is returned each time.
            ctypes does not implement original object return, always a new object is constructed. The same is true
            for all other ctypes object instances.
    """
    value: object

