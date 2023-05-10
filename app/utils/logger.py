import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)


class Logger(object):
    # colorama 支持以下 ANSI 颜色：
    RED_COLOR = Fore.RED  # 红色
    GREEN_COLOR = Fore.GREEN  # 绿色
    YELLOW_COLOR = Fore.YELLOW  # 黄色
    BLUE_COLOR = Fore.BLUE  # 蓝色

    # colorama 支持以下 style 操作
    RESET_ALL_STYLE = Style.RESET_ALL  # 重置所有颜色和样式

    @classmethod
    def info(cls, msg):
        cls.base(msg, cls.BLUE_COLOR)

    @classmethod
    def success(cls, msg):
        cls.base(msg, cls.GREEN_COLOR)

    @classmethod
    def waring(cls, msg):
        cls.base(msg, cls.YELLOW_COLOR)

    @classmethod
    def error(cls, msg):
        cls.base(msg, cls.RED_COLOR)

    @classmethod
    def base(cls, msg, start='', end=RESET_ALL_STYLE):
        print(f'{start}{msg}{end}')

    def __init__(self, *args, **kwargs):
        self.print(*args, **kwargs)

    @classmethod
    def print(cls, *args, **kwargs):
        if len(kwargs) > 0:
            cls.print_kv_data(**kwargs)
        if len(args) > 0:
            cls.print_list_data(*args)
        print('\n')

    @classmethod
    def print_kv_data(cls, **kwargs):
        if len(kwargs) > 0:
            for key, val in kwargs.items():
                print(f'================> key: {key}')
                val_type = type(val).__name__
                if val_type in ['list', 'tuple', 'set']:
                    cls.print(*val)
                elif val_type in ['dict']:
                    cls.print(**val)
                else:
                    kv = {key: val}
                    cls.success(f'================> {kv}')
                    cls.success(f'================> {key}.type: {val_type}')

    @classmethod
    def print_list_data(cls, *args):
        if len(args) > 0:
            for i in range(len(args)):
                item = args[i]
                print(f'================> item: {item}')
                item_type = type(item).__name__
                if item_type in ['list', 'tuple', 'set']:
                    cls.print(*item)
                elif item_type in ['dict']:
                    cls.print(**item)
                else:
                    cls.info(f'================> [{i}]: {item}')
                    cls.info(f'================> [{i}].type: {item_type}')


class LoggerPlus(object):
    # colorama 支持以下 ANSI 颜色：
    BLACK_COLOR = Fore.BLACK  # 黑色
    RED_COLOR = Fore.RED  # 红色
    GREEN_COLOR = Fore.GREEN  # 绿色
    YELLOW_COLOR = Fore.YELLOW  # 黄色
    BLUE_COLOR = Fore.BLUE  # 蓝色
    MAGENTA_COLOR = Fore.MAGENTA  # 洋红色
    CYAN_COLOR = Fore.CYAN  # 青色
    GREY_COLOR = Fore.WHITE  # 白色

    # colorama 支持以下 style 操作
    RESET_ALL_STYLE = Style.RESET_ALL  # 重置所有颜色和样式
    BOLD_STYLE = Style.BRIGHT  # 强调显示
    # WEAKEN_STYLE = Style.DIM  # 弱化显示
    NORMAL_STYLE = Style.NORMAL  # 正常显示

    @classmethod
    def info(cls, msg):
        cls.blue(msg=msg)

    @classmethod
    def success(cls, msg):
        cls.green(msg=msg)

    @classmethod
    def waring(cls, msg):
        cls.yellow(msg=msg)

    @classmethod
    def error(cls, msg):
        cls.red(msg=msg)

    @classmethod
    def base(cls, msg, start='', end=RESET_ALL_STYLE):
        print(f'{start}[ {msg} ]{end}')

    @classmethod
    def black(cls, msg):
        cls.base(msg, cls.BLACK_COLOR)

    @classmethod
    def grey(cls, msg):
        cls.base(msg, cls.GREY_COLOR)

    @classmethod
    def red(cls, msg):
        cls.base(msg, cls.RED_COLOR)

    @classmethod
    def green(cls, msg):
        cls.base(msg, cls.GREEN_COLOR)

    @classmethod
    def yellow(cls, msg):
        cls.base(msg, cls.YELLOW_COLOR)

    @classmethod
    def blue(cls, msg):
        cls.base(msg, cls.BLUE_COLOR)

    @classmethod
    def magenta(cls, msg):
        cls.base(msg, cls.MAGENTA_COLOR)

    @classmethod
    def cyan(cls, msg):
        cls.base(msg, cls.CYAN_COLOR)


if __name__ == '__main__':
    LoggerPlus.info('hello world')
    LoggerPlus.success('hello world')
    LoggerPlus.waring('hello world')
    LoggerPlus.error('hello world')
