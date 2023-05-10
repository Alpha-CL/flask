import os
import pkgutil
import sys

from werkzeug.utils import import_string


def import_all_module(file, name, path, prefix=None, callback=None, black_list=None) -> None:
    """
    :param file:        __file__    /xxx/xxx/xxx.ext
    :param name:        __name__    xxx
    :param path:        __path__    [/xxx/xxx/xxx]
    :param prefix:      custom package prefix name
    :param callback:    if file is package, execute callback
    :param black_list:  exclude file or package in black list
    """

    file_black_list = black_list or ["utils"]

    if prefix is None and name:
        prefix = name

    if isinstance(path, list) and len(path) > 0:
        current_file_path = path[0]
    else:
        current_file_path = os.path.dirname(file)
    current_file_name = os.path.basename(current_file_path)

    iter_modules = pkgutil.iter_modules([current_file_path])

    for _, child_file, is_pkg in iter_modules:
        if name is not None:
            module_path = f"{prefix}.{child_file}"
        else:
            module_path = f"{prefix}.{current_file_name}.{child_file}"

        try:
            if child_file not in file_black_list:
                if is_pkg and callback is not None and hasattr(callback, "__call__"):
                    callback(module_path)
                else:
                    __import__(module_path)
        except Exception as err:
            raise ImportError(f"import all module error: {err}")


def import_all(file, name, path, app=None, *args) -> None:
    """
    :param file:        __file__   [/xxx/xxx/xxx]
    :param name:        __name__   /xxx/xxx/xxx.py
    :param path:        __path__
    :param app:         flask_app
    :param args:        prefix, black_list
    """

    def callback(module_path):
        import_blueprint(module_path, app)

    import_all_module(file, name, path, callback=callback, *args)


def import_blueprint(blueprint, app) -> None:
    import_string(blueprint).init_app(app)


def import_parent_package(path=None) -> None:
    if type(path) == "string":
        sys.path.append(path)
    else:
        sys.path.append("..")