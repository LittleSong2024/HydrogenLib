from typing import Union, Iterable, Tuple


def mapping(stream, in_min, in_max, out_min, out_max):
    return (stream - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def pack_variable_length_int(x: int):
    """
    将整数打包为可变长格式
    """
    res = bytearray()
    while True:
        byte = x & 0x7F
        x >>= 7
        if x:
            byte |= 0x80
        res.append(byte)
        if not x:
            break
    return bytes(res)


def unpack_variable_length_int(data: Union[bytes, bytearray, Iterable[int]]) -> Tuple[int, int]:
    """
    将可变长格式的整数字节串解包
    返回: 解包后的整数, 解包使用的字节数
    """
    result = 0
    shift = 0
    count = 0
    for byte in data:
        result |= (byte & 0x7F) << shift
        shift += 7
        if byte & 0x80 == 0:
            break
        count += 1
    return result, count + 1
