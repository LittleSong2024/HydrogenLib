import struct
from decimal import Decimal
from .type_func import pack_variable_length_int, unpack_variable_length_int


def neopack(data):
    """
    对基本Struct模块的功能进行一定的改进的方法
    **Format Mro**

    - x           pad byte
    - c           char
    - b           int8
    - B           uint8
    - h           int16
    - H           uint16
    - i           int32
    - I           uint32
    - l           int64
    - L           uint64
    - f           float
    - d           double
    - s           char[]
    - q           long long
    - Q           unsigned long long
    - e           half float
    - f           float
    - d           double
    - n           long long
    - N           unsigned long long
    - p           bytes
    - P           int(Point)
    - ?           bool
    """
    data_type = type(data)
    if data_type == int:
        return pack_variable_length_int(data)
    elif data_type in [float, Decimal]:
        # 0.00001
        count = 0
        while data-int(data) != 0:
            data *= 10
            count += 1
        part1 = pack_variable_length_int(count)
        part2 = pack_variable_length_int(int(data))
        return part1 + part2
    elif data_type == str:
        return data.encode()
    elif data_type == bytes:
        return data
    elif data_type == bool:
        return struct.pack("<?", data)
    else:
        raise TypeError("unsupported data type: {}".format(data_type))


def neounpack(data_type, data):
    if data_type == int:
        return unpack_variable_length_int(data)[0]
    elif data_type in [float, Decimal]:
        offset, length = unpack_variable_length_int(data)
        bytes_, _ = unpack_variable_length_int(data[length:])
        print(bytes_)
        return data_type(bytes_) / (10 ** offset)
    elif data_type == str:
        return data.decode()
    elif data_type == bytes:
        return data
    elif data_type == bool:
        return struct.unpack("<?", data)[0]
    else:
        raise TypeError("Unsupported data type: {}".format(data_type))
