import os
import urllib
from urllib.parse import quote_plus
from redis import StrictRedis

from dotenv import load_dotenv

import colorama

from app.utils.logger import Logger

colorama.init(autoreset=True)

BASE_DIR = os.path.abspath(os.path.dirname('../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


def escape_special_chars(string):
    """
    转义字符串中的特殊字符
    """
    special_chars = [":", "/", "@", "?", "=", "+", "&"]
    for char in special_chars:
        string = string.replace(char, quote_plus(char))
    return string


def encode_url(url):
    parse_url = urllib.parse.urlparse(url)

    scheme = escape_special_chars(parse_url.scheme)
    if parse_url.scheme.find('+') != -1:
        dialect, driver = parse_url.scheme.split('+')
        scheme = f'{escape_special_chars(dialect)}+{escape_special_chars(driver)}'
    password = escape_special_chars(parse_url.password)
    user = escape_special_chars(parse_url.username)
    port = escape_special_chars(str(parse_url.port))
    db = escape_special_chars(parse_url.path[1:])
    host = escape_special_chars(parse_url.hostname)

    return f'{scheme}://{str(user) + "." if user else ""}{password}@{host}:{port}/{db}'


def create_url(dialect=None, driver=None, user=None, password=None, host=None, port=None, db=None, url=None):
    """
    '{dialect+driver}://{user}:{password}@{host}:{port}/{db}'
    特殊字符需要转译
    """
    if url is None:
        password = escape_special_chars(password)
        url = f'{dialect}+{driver}://{user}:{password}@{host}:{port}/{db}'
        url = f'{encode_url(url)}'
    return url


def get_connect(url=None, **kwargs):
    if url is None:
        redis_connect = StrictRedis(decode_responses=True, **kwargs)
    else:
        redis_connect = StrictRedis.from_url(url)
    print(f'================> url: {url}')
    print(f'================> kwargs: {kwargs}')
    return redis_connect


class DBRedisSession(object):

    def __init__(
            self,
            dialect=None,
            driver=None,
            password=None,
            host=None,
            port=None,
            db=None,
            url=None,
    ):
        self.__dialect = dialect or 'redis'
        self.__driver = driver or ''
        self.__password = password or os.getenv('REDIS_PASSWORD')
        self.__host = host or os.getenv('REDIS_HOST') or 'localhost'
        self.__port = port or os.getenv('REDIS_PORT') or 6379
        self.__db = db or os.getenv('REDIS_DB') or 'dev'

        self.__url = url or os.getenv('REDIS_DB_URL')

    def __getattr__(self, command):
        def _(*args, **kwargs):
            return getattr(self._connect, command)(*args, **kwargs)

        return _

    def __enter__(self):
        Logger.info(msg=f'Open redis client')
        connect = get_connect(host=self.__host, port=self.__port, password=self.__password, db=self.__db,
                              url=self.__url)
        is_connect = connect.ping()
        if is_connect:
            Logger.success(msg=f'Success connect redis client: {connect}')
            self._connect = connect
            return self

    def __exit__(self, *exc_infos):
        if self._connect and exc_infos == (None, None, None):
            self.connect.close()
            Logger.info(msg=f'closed redis client')
        else:
            Logger.error(msg=f'Redis session exit error: {exc_infos}')

    @property
    def connect(self):
        return self._connect

    def clear_db(self):
        return self.connect.flushdb()

    def ping_server(self):
        return self.connect.ping()

    def get_type(self, key=None):
        if self.is_type(key, 'str'):
            return self.connect.type(key).decode('utf-8')

    def is_exists_key(self, key=None, is_log=True):
        if self.is_type(key, 'str'):
            is_exists = bool(self.connect.exists(key))
            if is_exists:
                return is_exists
            else:
                is_log and Logger.error(f'"{key}" does not exist.')
                return False

    def is_safe_key(self, key, is_log=True):
        if self.is_type(key, 'str'):
            is_safe = self.get_type(key) == self.NONE_TYPE
            if is_safe:
                return is_safe
            else:
                key_type = self.get_type(key)
                is_log and Logger.error(f'"{key}" already exists, its type is "{key_type}"')
                return False

    def is_target_type(self, key, target_type, is_log=True):
        if self.is_type(key, 'str'):
            key_type = self.get_type(key)
            type_is_equal = key_type == target_type
            if type_is_equal:
                return type_is_equal
            else:
                key_type = self.get_type(key)
                is_log and Logger.error(f'{key} type is not {target_type}, its type is {key_type}')
                return False

    def is_str_type(self, key=None, **kwargs):
        return self.is_target_type(key, self.STRING_TYPE, **kwargs)

    def is_list_type(self, key=None, **kwargs):
        return self.is_target_type(key, self.LIST_TYPE, **kwargs)

    def is_set_type(self, key=None, **kwargs):
        return self.is_target_type(key, self.SET_TYPE, **kwargs)

    def is_order_set_type(self, key=None, **kwargs):
        return self.is_target_type(key, self.ORDER_SET_TYPE, **kwargs)

    def is_map_type(self, key=None, **kwargs):
        return self.is_target_type(key, self.MAP_TYPE, **kwargs)

    def is_examine_target(self, key, target_type, **kwargs):
        is_exists_key = self.is_exists_key(key, **kwargs)
        if not is_exists_key:
            return
        is_target_type = self.is_target_type(key, target_type, **kwargs)

        return is_exists_key and is_target_type

    def is_examine_str(self, key=None, **kwargs):
        return self.is_examine_target(key, self.STRING_TYPE, **kwargs)

    def is_examine_list(self, key=None, **kwargs):
        return self.is_examine_target(key, self.LIST_TYPE, **kwargs)

    def is_examine_set(self, key=None, **kwargs):
        return self.is_examine_target(key, self.SET_TYPE, **kwargs)

    def is_examine_order_set(self, key=None, **kwargs):
        return self.is_examine_target(key, self.ORDER_SET_TYPE, **kwargs)

    def is_examine_map(self, key=None, **kwargs):
        return self.is_examine_target(key, self.MAP_TYPE, **kwargs)

    def delete_target(self, name, *names):
        all_name = [*names]
        if self.is_type(name, ['list', 'tuple']):
            all_name = [*name, *names]
        elif self.is_type(name, 'str'):
            all_name = [name, *names]
        result = self.connect.delete(*all_name)
        if result:
            target_type = self.get_type(name)
            Logger.success(f'Success delete {all_name}, its type is {target_type}')
            return result

    def delete_str(self, *key):
        return self.delete_target(*key)

    def delete_list(self, *name):
        return self.delete_target(*name)

    def delete_map(self, *name):
        return self.delete_target(*name)

    """
    string      # 字符串       key: val
    list        # 列表        [ val1, val2, val3 ]
    set         # 集合        { item, item, item }
    order_set   # 有序集合     { item1, item2, item3 }
    hash        # 字典        { key: val }
    """

    STRING_TYPE = 'string'
    LIST_TYPE = 'list'
    SET_TYPE = 'set'
    ORDER_SET_TYPE = 'sorted set'
    MAP_TYPE = 'hash'
    NONE_TYPE = 'none'
    ALL_TYPE = [STRING_TYPE, LIST_TYPE, SET_TYPE, ORDER_SET_TYPE, MAP_TYPE, NONE_TYPE]

    """
    hash 中的键不能重复，如果设置相同键的字段值，会覆盖之前的数据
    如果 hash 中的字段值是整数类型，可以使用 hincrby(key, field, amount) 方法对其进行原子性增加或减少操作

    hget(key, field):从哈希中获取指定字段的值
    hset(key, field, value):将哈希中的指定字段设置为给定的值
    hmget(key, fields):获取哈希中多个字段的值
    hmset(key, mapping):同时设置哈希中多个字段的值
    hkeys(key):获取哈希中所有的字段名
    hvals(key):获取哈希中所有的值
    hgetall(key):获取哈希中所有的字段名和对应的值
    hlen(key):获取哈希中字段的数量
    hdel(key, *fields):从哈希中删除一个或多个字段
    hexists(key, field):判断哈希中指定字段是否存在
    hincrby(key, field, amount=1):将哈希中指定字段的值增加指定的数量
    hincrbyfloat(key, field, amount=1.0):将哈希中指定字段的值增加指定的浮点数
    hscan(key, cursor=0, match=None, count=None):迭代哈希中的所有字段名和对应的值
    """

    """
    set(key, value, ex=None, px=None, nx=False, xx=False):  设置指定 key 的值可选参数 ex 或 px 用于设置过期时间，nx 或 xx 用于设置当 key 不存在或存在时的行为
    get(key):                                   获取指定 key 的值
    mget(keys, *args):                          获取多个 key 的值
    mset(mapping):                              同时设置多个 key 的值
    incr(key, amount=1):                        将指定 key 的值增加指定的整数
    decr(key, amount=1):                        将指定 key 的值减少指定的整数
    append(key, value):                         将指定字符串附加到指定 key 的值的末尾
    getrange(key, start, end):                  获取指定 key 的值的子字符串
    setrange(key, offset, value):               用指定的值替换指定 key 的值的子字符串
    strlen(key):                                获取指定 key 的值的长度
    setex(key, time, value):                    设置指定 key 的值，并将其设置为在指定时间后过期
    psetex(key, time_ms, value):                设置指定 key 的值，并将其设置为在指定时间（以毫秒为单位）后过期
    setnx(key, value):                          仅在指定 key 不存在时设置其值
    getset(key, value):                         设置指定 key 的值，并返回其之前的值
    incrbyfloat(key, amount=1.0):               将指定 key 的值增加指定的浮点数
    bitcount(key, start=None, end=None):        计算指定 key 的值中包含的位数
    bitop(operation, dest, *keys):              对指定 key 的值执行位运算，并将其结果存储在指定的 key 中
    bitpos(key, bit, start=None, end=None):     查找指定 key 的值中指定位的位置
    getbit(key, offset):                        获取指定 key 的值中指定位的值
    setbit(key, offset, value):                 设置指定 key 的值中指定位的值
    """

    """ str method start """

    def add_str(self, key, val, second=None, millisecond=None, params=None, operation_type='create',
                **kwargs):
        """
        有且仅当 key 不存在时，才添加

        strict: bool
        ex - second: int        # 过期时间( 秒 )
        px - millisecond: int   # 过期时间( 毫秒 )
        nx                      # 如果键不存在， 才设置键值 默认为 False    # 若设置为 Ture, 则等价于 setnx(name, value)
        xx                      # 如果键已经存在，才设置键值 默认为 False
        """
        if (self.is_str_type(key, is_log=False) and operation_type == 'update') or (
                self.is_safe_key(key) and operation_type == 'create'):

            key = str(key) if type(key).__name__ != 'str' else key
            val = self.encode_2_str(val) if type(val).__name__ != 'str' else val

            params = {}
            if operation_type == 'create':
                params = {'nx': True, 'xx': False}
            elif operation_type == 'update':
                params = {'nx': False, 'xx': True}
            if second and self.is_type(second, 'int'):
                return self.connect.set(name=key, value=val, ex=second, **params, **kwargs)
            elif millisecond and self.is_type(millisecond, 'int'):
                return self.connect.set(name=key, value=val, px=millisecond, **params, **kwargs)
            else:
                return self.connect.set(name=key, value=val, **params, **kwargs)

    def add_all_str(self, strs_dict=None, **kwargs):
        all_dict_params = self.get_dict_params(strs_dict, **kwargs)
        all_safe_dict = {}
        for key, val in all_dict_params.items():
            if self.is_safe_key(key):
                all_safe_dict[key] = self.encode_2_str(val)
        if len(all_safe_dict) > 0:
            return self.connect.mset(self.str_dict__val_2_str(all_safe_dict))

    def del_str(self, key):
        return self.del_all_str(key)

    def del_all_str(self, keys=None, *args):
        all_list_params = self.get_list_params(keys, *args)
        all_safe_key = [key for key in all_list_params if self.is_examine_str(key)]
        if len(all_safe_key) > 0:
            self.connect.delete(*all_safe_key)

    def update_str(self, key, val, second=None, millisecond=None, **kwargs):
        if self.is_str_type(key):
            return self.add_str(key, val, second=second, millisecond=millisecond, operation_type='update', **kwargs)

    def update_all_str(self, strs_dict=None, **kwargs):
        if self.is_type(strs_dict, 'dict') or len(kwargs) > 0:
            all_dict_params = self.get_dict_params(strs_dict, **kwargs)
            all_safe_dict_params = {}
            for key, val in all_dict_params.items():
                if self.is_str_type(key):
                    key = str(key)
                    val = self.encode_2_str(val)
                    all_safe_dict_params[key] = val
            if len(all_safe_dict_params) > 0:
                self.connect.mset(all_safe_dict_params)
        elif self.is_type(strs_dict, 'list'):
            all_list_params = strs_dict
            if len(all_list_params) > 0:
                for params in all_list_params:
                    if self.is_type(params, 'tuple'):
                        key, val, *_ = params
                        if key and val:
                            self.update_str(*params)
                    elif self.is_type(params, 'dict'):
                        key, val, *_ = params
                        if key and val:
                            self.update_str(str(key), self.encode_2_str(val), **params)

    def get_str(self, key):
        if self.is_examine_str(key):
            bytes_str = self.connect.get(key)
            return self.bytes_2_str(bytes_str)

    def get_all_str(self, keys=None, *args):
        all_keys = self.get_list_params(keys, *args)
        all_safe_key = [key for key in all_keys if self.is_str_type(key)]
        all_safe_value = self.bytes_list_decode(self.connect.mget(all_safe_key))
        result = self.list_zip_dict(all_safe_key, all_safe_value)
        return result if len(result) else None

    def get_str_slice(self, key, start=0, end=-1):
        if self.is_examine_str(key) and self.is_safe_index(key, start, end):
            return self.connect.getrange(key, start, end)

    def str_len(self, key=None):
        if self.is_examine_str(key):
            return self.connect.strlen(key)

    def add_token(self, key, val, second, millisecond):
        return self.add_str(key, val, second=second, millisecond=millisecond)

    def del_token(self, key):
        return self.del_str(key)

    def update_token(self, key, val, second, millisecond):
        return self.update_str(key, val, second=second, millisecond=millisecond)

    def get_token(self, key):
        return self.get_str(key)

    """ str method end """

    """
    lpush(name, *values):           将一个或多个值插入到列表的头部
    rpush(name, *values):           将一个或多个值插入到列表的尾部
    lpop(name):                     删除并返回列表的头部元素
    rpop(name):                     删除并返回列表的尾部元素
    lrange(name, start, end):       返回列表中指定范围内的元素
    llen(name):                     返回列表的长度
    lindex(name, index):            返回列表中指定位置的元素
    lrem(name, count, value):       从列表中删除指定的值
    lset(name, index, value):       设置列表中指定位置的元素值
    ltrim(name, start, end):        保留指定范围内的元素，其它元素全部删除
    """

    """ list method start """

    def add_list(self, name, items_list, *values):
        if self.is_safe_key(name):
            all_values = self.get_list_params(items_list, *values)
            str_list = self.any_list_encode(all_values)
            return self.connect.lpush(name, *str_list)

    def push_many_items_2_list(self, name, *values):
        if self.is_examine_list(name):
            str_list = self.any_list_encode(values)
            return self.connect.lpush(name, *str_list)

    def unshift_many_items_2_list(self, name, *values):
        if self.is_examine_list(name):
            str_list = self.any_list__item_2_str(values)
            return self.connect.rpush(name, *str_list)

    def pop_item_in_list(self, name):
        if self.is_examine_list(name):
            return self.connect.lpop(name)

    def shift_item_in_list(self, name):
        if self.is_examine_list(name):
            return self.connect.rpop(name)

    def get_list(self, name):
        if self.is_examine_list(name):
            return self.slice_list(name, 0, -1)

    def get_list_item_by_index(self, name, i):
        if self.is_examine_list(name):
            return self.connect.lindex(name, i)

    def update_list_item_by_index(self, name, i, val):
        if self.is_examine_list(name):
            return self.connect.lset(name, i, val)

    def del_list_item_by_index(self, name, i, count=1):
        if self.is_examine_list(name):
            return self.connect.lrem(name, count, i)

    def get_list_slice(self, key, start=0, end=-1):
        if self.is_examine_list(key):
            bytes_list = self.connect.lrange(key, start, end)
            return self.bytes_list_decode(bytes_list)

    def pop_other_items_in_list(self, name, start, end):
        if self.is_examine_list(name):
            return self.connect.ltrim(name, start, end)

    def list_len(self, key=None):
        if self.is_examine_list(key):
            return self.connect.llen(key)

    def has_key_in_list(self, name, key):
        if self.is_examine_list(name):
            all_items = self.get_list(name)
            if len(all_items) > 0:
                return key in all_items

    """ list method end """

    """
    hset(name, key, value):                         设置指定哈希集中指定字段的值
    hget(name, key):                                获取指定哈希集中指定字段的值
    hmset(name, mapping):                           同时设置多个哈希集字段的值
    hmget(name, keys, *args):                       同时获取多个哈希集字段的值
    hgetall(name):                                  获取指定哈希集中所有字段和值
    hlen(name):                                     获取指定哈希集中字段的数量
    hkeys(name):                                    获取指定哈希集中所有字段
    hvals(name):                                    获取指定哈希集中所有值
    hdel(name, *keys):                              删除指定哈希集中一个或多个字段
    hexists(name, key):                             判断指定哈希集中是否存在指定字段

    hincrby(name, key, amount=1):                   将指定哈希集中指定字段的值增加给定的整数
    hincrbyfloat(name, key, amount=1.0):            将指定哈希集中指定字段的值增加给定的浮点数
    hsetnx(name, key, value):                       只有在指定哈希集中指定字段不存在时，才设置该字段的值
    hscan(name, cursor=0, match=None, count=None):  迭代遍历指定哈希集中的所有字段和值
    """

    """ map method start """

    def add_map(self, name, mapping=None, key=None, val=None, operation_type='create', **kwargs):
        if operation_type == 'update' or (self.is_safe_key(name) and operation_type == 'create'):
            all_dict_params = self.get_dict_params(mapping, **kwargs)
            if key and val:
                all_dict_params = {**{key: val}, **all_dict_params}
            safe_map = {key: self.encode_2_str(val) for key, val in all_dict_params.items() if True}
            if len(safe_map) > 0:
                return self.connect.hset(name, mapping=safe_map, **kwargs)

    def del_item_in_map(self, name, key):
        return self.del_many_items_in_map(name, key)

    def del_many_items_in_map(self, name, *keys):
        if self.is_examine_map(name):
            return self.connect.hdel(name, *keys)

    def update_item_in_map(self, name, key, val, **kwargs):
        if self.is_examine_map(name) and self.is_type(key, 'str'):
            val = self.encode_2_str(val)
            return self.add_map(name, key, val, operation_type='update', **kwargs)

    def update_many_items_in_map(self, name, items_map, **kwargs):
        all_dict_params = self.get_dict_params(items_map, **kwargs)
        return self.add_map(name, mapping=all_dict_params, operation_type='update', **kwargs)

    def get_map(self, name):
        if self.is_examine_map(name):
            result = self.connect.hgetall(name)
            if self.is_type(result, 'dict') and len(result) > 0:
                return self.bytes_dict_decode(result)
            else:
                return result

    def get_item_in_map(self, name, key):
        if self.is_examine_map(name) and self.has_key_in_map(name, key):
            val = self.connect.hget(name, key)
            return self.bytes_decode(val) if val else None

    def get_many_items_in_map(self, name, keys, *args):
        if self.is_examine_map(name):
            all_list_params = self.get_list_params(keys, *args)
            all_safe_key = [key for key in all_list_params if self.has_key_in_map(name, key)]
            if len(all_safe_key) > 0:
                result = self.connect.hmget(name, all_safe_key)
                all_safe_values = self.bytes_list_decode(result)
                return self.list_zip_dict(all_safe_key, all_safe_values)

    def map_keys(self, name):
        if self.is_examine_map(name):
            return self.connect.hkeys(name)

    def map_values(self, name):
        if self.is_examine_map(name):
            return self.connect.hvals(name)

    def map_len(self, name=None):
        if self.is_examine_map(name):
            return self.connect.hlen(name)

    def has_key_in_map(self, name, key):
        if self.is_examine_map(name):
            return self.connect.hexists(name, key)

    """ map method end """

    """
    元素唯一，无序排列，若已有该元素，则不会重复插入

    sadd(name, *items)          插入元素，可以一次插入多个元素
    srem(name, *items)          移除元素，可以一次移除多个元素
    scard(name)                 获取元素个数
    sismember(name, item)       判断元素是否存在于集合中
    smembers(name)              获取集合中所有元素
    srandmember(name)           随机获取集合中的一个元素
    spop(name)                  随机弹出集合中的一个元素
    sinter(names)               求多个集合的交集
    sunion(names)               求多个集合的并集
    sdiff(set1, set2)           求两个集合的差集
    """

    """
    元素唯一，有序排列，若已有该元素，则不会重复插入

    @param {name} 表示有序集合的名称
    @param {value} 表示有序集合的成员
    @param {mapping} 表示score-member对的字典或映射
    @param {min和max} 表示score的范围
    @param {start和end} 表示排名的范围
    @param {keys} 表示有序集合的名称列表
    @param {aggregate} 表示聚合函数
    @param {dest} 表示目标有序集合的名称
    @param {num} 表示返回结果的数量
    @param {score_cast_func} 表示score的类型转换函数

    zadd(name, mapping):                        将一个或多个score-member对添加到有序集合name中
    zcard(name):                                返回有序集合name的成员数
    zcount(name, min, max):                     返回有序集合name中score在[min,max]范围内的成员数
    zincrby(name, amount, value):               将有序集合name中value的score增加amount
    zinterstore(dest, keys, aggregate=None):    将多个有序集合keys的交集存储到dest中
    zlexcount(name, min, max):                  返回有序集合name中成员在[min, max]字典范围内的数量
    zrange(name, start, end, desc=False, withscores=False, score_cast_func=float):      返回有序集合name中排名在[start,end]之间的成员
    zrangebylex(name, min, max, start=None, num=None):                                  返回有序集合name中成员在[min,max]字典范围内的成员
    zrevrange(name, start, end, withscores=False, score_cast_func=float):               返回有序集合name中排名在[start,end]之间的成员，按score值从大到小排序
    zrangebyscore(name, min, max, start=None, num=None, withscores=False, score_cast_func=float): 返回有序集合name中score在[min,max]范围内的成员
    zrank(name, value):                         返回有序集合name中value的排名，按score从小到大排序
    zrevrank(name, value):                      返回有序集合name中value的排名，按score从大到小排序
    zrem(name, values):                         从有序集合name中删除values
    zremrangebylex(name, min, max):             从有序集合name中删除成员在[min,max]字典范围内的成员
    zremrangebyrank(name, start, end):          从有序集合name中删除排名在[start,end]之间的成员
    zremrangebyscore(name, min, max):           从有序集合name中删除score在[min,max]范围内的成员
    zrevrangebyscore(name, max, min, start=None, num=None, withscores=False, score_cast_func=float): 返回有序集合name中score在[min,max]范围内的成员，按score从大到小排序
    zscore(name, value):                        返回有序集合name中value的score
    zunionstore(dest, keys, aggregate=None):    将多个有序集合keys的并集存储到dest中
    """

    @classmethod
    def get_list_params(cls, target, *args):
        params = [*args]
        if target and cls.is_type(target, ['list', 'tuple']):
            params = [*target, *params]
        elif target and cls.is_type(target, 'str'):
            params = [target, *params]
        return params

    @classmethod
    def get_dict_params(cls, target, **kwargs):
        params = {**kwargs}
        if target and cls.is_type(target, 'dict'):
            params = {**target, **params}
        return params

    @classmethod
    def filter_safe_dict(cls, any_list):
        pass

    @classmethod
    def is_safe_index(cls, name, _min, _max):
        key_type = cls.get_type(name)
        if key_type == cls.STRING_TYPE:
            index_max = cls.str_len(name)
        elif key_type == cls.LIST_TYPE:
            index_max = cls.list_len(name)
        elif key_type == cls.MAP_TYPE:
            index_max = cls.map_len(name)
        else:
            return False
        index_min = 0
        if _min < index_min or _max > index_max:
            Logger.error('index out of bounds')
            return False
        return True

    @classmethod
    def is_type(cls, target, target_type=None, *last_type):
        if target and target_type:
            if type(target_type).__name__ in ['list', 'tuple']:
                if len(last_type) > 0:
                    return type(target).__name__ in [*target_type, *last_type]
                else:
                    return type(target).__name__ in target_type
            else:
                return type(target).__name__ == target_type
        else:
            return type(target).__name__

    @classmethod
    def bytes_2_str(cls, target):
        return target.decode('utf-8') if cls.is_type(target, 'bytes') else target

    @classmethod
    def str_dict__val_2_str(cls, str_dict):
        if cls.is_type(str_dict, 'dict'):
            result = dict(str_dict)
            for key, val in result.items():
                if cls.is_type(val, 'str'):
                    str_dict.update({key: str(val)})
            return result
        else:
            return str_dict

    @classmethod
    def encode_2_str(cls, target):
        if cls.is_type(target, 'bool'):
            return str(int(target))
        if cls.is_type(target, 'NoneType'):
            return str(target).lower()
        else:
            return str(target)

    @classmethod
    def bytes_decode(cls, target):
        if cls.is_type(target, 'bytes'):
            str_target = cls.bytes_2_str(target)
        else:
            str_target = str(target)
        if str_target in ['0', '1']:
            return bool(int(str_target))
        elif str.isdigit(str_target):
            return int(str_target)
        elif str.isdigit(str_target) and isinstance(float(str_target), float):
            return float(str_target)
        elif str_target == 'none':
            return None

    @classmethod
    def any_list_encode(cls, any_list):
        if isinstance(any_list, (list, tuple)) and len(any_list) > 0:
            result = []
            for i in range(len(any_list)):
                item = any_list[i]
                str_item = cls.encode_2_str(item)
                result.append(str_item)
            return result
        else:
            return any_list

    @classmethod
    def any_dict_encode(cls, any_dict):
        if isinstance(any_dict, dict) and len(any_dict) > 0:
            result = {}
            for key, val in any_dict.items():
                key = str(key)
                val = cls.encode_2_str(val)
                result[key] = val
            return result
        else:
            return any_dict

    @classmethod
    def bytes_list_decode(cls, bytes_list):
        if isinstance(bytes_list, (list, tuple)) and len(bytes_list) > 0:
            result = []
            for i in range(len(bytes_list)):
                bytes_item = bytes_list[i]
                item = cls.bytes_decode(bytes_item)
                result.append(item)
            return result
        else:
            return bytes_list

    @classmethod
    def bytes_dict_decode(cls, bytes_dict):
        if cls.is_type(bytes_dict, 'dict') and len(bytes_dict) > 0:
            result = {}
            for key, val in bytes_dict.items():
                key = cls.bytes_2_str(key)
                val = cls.bytes_decode(val)
                result[key] = val
            return result
        else:
            return bytes_dict

    @classmethod
    def list_zip_dict(cls, keys, values):
        if cls.is_type(keys, ['list', 'tuple']) and cls.is_type(keys, ['list', 'tuple']) and len(keys) == len(values):
            if len(keys) > 0 and len(values) > 0:
                return dict(zip(keys, values))


class DBRedisException(Exception):

    def __init__(self, msg):
        self.msg = msg


if __name__ == '__main__':
    db_host = os.getenv('REDIS_HOST') or 'localhost'
    db_port = os.getenv('REDIS_PORT') or 3306
    db_password = os.getenv('REDIS_PASSWORD')
    db_db = os.getenv('REDIS_DB') or 'dev'

    db_url = os.getenv('REDIS_DB_URL')

    with DBRedisSession() as orm:
        session = orm.connect

        # res = orm.clear_db()
