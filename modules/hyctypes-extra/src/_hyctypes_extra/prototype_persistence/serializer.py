from ..._hyctypes.cfunction import CPrototype


def prototype_to_dict(prototype: CPrototype):
    return {
        'identifier': prototype.name_or_ordinal,
        'return_type': str(prototype.restype),
        'argument_types': [str(argtype) for argtype in prototype.argtypes],
        'paramflags': prototype.paramflags,
    }
