from types import SimpleNamespace
from flask import jsonify
from pymysql.cursors import Cursor


# instance_state = db.session.query(DemoModel).filter(DemoModel.id == 1).all()
def instance_state_2_dict(instance_state, to_jsonify=None):
    res_dict = {}
    __dict__ = instance_state.__dict__
    if "_sa_instance_state" in __dict__:
        del __dict__['_sa_instance_state']
    res_dict.update(__dict__)
    return __to_jsonify(res_dict) if to_jsonify else res_dict


# instance_state_list = db.session.query(DemoModel).all()
def instance_state_list_2_dict_list(instance_list, to_jsonify=None):
    map_list = []
    for v in instance_list:
        v_map = instance_state_2_dict(v)
        map_list.append(v_map)
    return __to_jsonify(map_list) if to_jsonify else map_list


# cursor = db.session.execute(sql).cursor
def cursor_2_dict_list(cursor):
    if isinstance(cursor, Cursor):
        name_tuple = [i[0] for i in cursor.description]
        return [dict(zip(name_tuple, value_tuple)) for value_tuple in cursor]


def dict_2_obj(dict_obj):
    class Dict(dict):
        __setattr__ = dict.__setitem__
        __getattr__ = dict.__getitem__

    if not isinstance(dict_obj, dict):
        return dict_obj
    d = Dict()
    for k, v in dict_obj.items():
        d[k] = dict_2_obj(v)
    return d


def dict_2_sobj(dict_obj):
    return SimpleNamespace(**dict_obj)


def __to_jsonify(data):
    return jsonify(data)
