import warnings
from collections import OrderedDict
from typing import Literal, Unpack

from _hycore.typefunc import iter_annotations, iter_attributes
from _hycore.data_structures import Visited

from .models import _FieldValidator, ModelConfig, Field, BaseModelConfig


def field_validator(name):
    def decorator(func):
        return _FieldValidator(func, name)

    return decorator


class BaseModel:
    def __init_subclass__(cls, **kwargs: Unpack[BaseModelConfig]):
        cls.__model__ = ModelConfig()
        cls.__fields__ = dct = OrderedDict[str, Field]()  # 记录 fields

        count_optional_field = 0  # 记录有默认值的字段有没有出现
        is_break = False

        for name, typ, value in iter_annotations(cls):
            dct[name] = field = Field(name, typ, value)

            if field.has_default():
                count_optional_field += 1

            elif count_optional_field:
                is_break = True

            if count_optional_field and is_break:
                field.keyword_only = True  # 一段默认值字段序列后的所有字段都只能作为关键字参数

            setattr(cls, name, field)

        count_required_field = len(dct) - count_optional_field

        for name, value in iter_attributes(cls):  # 处理验证器
            if isinstance(value, _FieldValidator):
                if value.name not in dct:
                    warnings.warn(f"FieldValidator {value.name} not found in {cls.__name__}")
                    continue  # 跳过这个无效的验证器

                dct[value.name].validator = value  # 绑定验证器

        cls.__field_counts__ = {
            'optional': count_optional_field,
            'required': count_required_field,
        }  # type: dict[Literal['optional', 'required'], int]

    def __init__(self, *args, **kwargs):
        vis = Visited()
        count_opt = count_req = 0

        for (name, field), arg in zip(self.__fields__.items(), args):
            if field.keyword_only:
                raise TypeError('Too many arguments')  # 如果 args 的长度是正确的, 那么不会出现遍历到 keyword_only 的情况
            
            if field.has_default():
                count_opt += 1
            else:                      # 分别对两种参数计数
                count_req += 1

            vis[name] = True

            setattr(self, field.name, arg)  # 赋值, 验证会自动进行

        for field, value in kwargs.items():
            if field not in self.__fields__:  # 首先不能出现不存在的字段
                raise TypeError(f"Unexcept field {field}")
            if field in vis:  # 其次不能出现重复的字段
                raise TypeError(f"{field} has been assigned")

            setattr(self, field, value)

        # TODO: 处理未填写的必须字段

# TODO: 实现类型验证
