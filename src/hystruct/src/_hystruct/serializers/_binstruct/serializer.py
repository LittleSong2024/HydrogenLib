from .struct_abc import Serializer, Handler, SimpleTypes
from ...._hycore import neostruct, type_func


class SimpleTypes_Handler(Handler):
    def packable(self, data):
        return isinstance(data, SimpleTypes)

    def pack(self, serializer, data):
        return type_func.get_type_name(data). + neostruct.neopack(data)

    def


