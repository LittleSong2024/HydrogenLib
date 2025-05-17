from src.hydrogenlib._hysocket.protrol_abc import HySocketProtrol
from .._hycore.neostruct import pack_variable_length_int, unpack_variable_length_int


def build_protrol_head(protrol):
    """
    构建protrol头
    返回结果为 b'<protrol_id>@<protrol_version>'

    :param protrol: 协议实例
    :return: bytes
    """
    if not isinstance(protrol, HySocketProtrol):
        raise TypeError('protrol must be a HySocketProtrol')
    return protrol.final_id + b'@' + '.'.join(map(str, protrol.version)).encode()


def parse_protrol_head(head: bytes):
    """
    解析protrol头
    返回结果为 (protrol_id, protrol_version)
    """

    # real_head = head[1:-1]  # 去掉头尾的[]
    split_pos = head.find(b'@')
    if split_pos == -1:
        raise ValueError('protrol head is not valid')

    left, right = head[:split_pos], head[split_pos + 1:].decode()

    final_id = left
    version = tuple(map(int, right.split('.')))

    return final_id, version


def build_protrol_tail(protrol, length):
    return build_protrol_head(protrol) + b':' + pack_variable_length_int(length)

