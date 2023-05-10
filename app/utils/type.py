base_type_list = (
    str,  # 字符串
    int, float, complex,  # 数字
    bool,  # 布尔
)
object_type_list = (
    list, tuple, range,  # 列表
    dict,  # 对象
    set, frozenset,  # 集合
    bytes, bytearray, memoryview,  # 字节
    None,  # 未定义，占位
)
false_list = [None, False, 0, '', [], (), {}]

"""
type(target)                          # 只能判断类型，返回一个对象的类类型( 即对象所属的类 ), 无法判断继承关系
isinstance(son, parent)               # 用于判断一个对象是否是指定类的实例( 包括其子类的实例 )
issubclass(instance, class)           # 用于判断一个类是否是另一个类的派生类( 即子类 )
"""


def get_type(target):
    return type(target).__name__


def is_clazz_instance(instance, clazz):
    return isinstance(instance, clazz)


def is_inherit_clazz(sub_clazz, clazz):
    return issubclass(sub_clazz, clazz)


def to_bool(target):
    for f in false_list:
        if target == f:
            return False
    return True


def to_str(target):
    return str(target)


def to_int(target):
    return int(target)


def to_float(target):
    return float(target)


def is_type(target, data_type):
    target_type = get_type(target)
    return target_type == data_type


def is_func(target):
    return hasattr(target, '__call__')


if __name__ == '__main__':
    pass
