import fileinput
import linecache
import os
import re
import shutil


class FileHandle(object):
    __file_path = None
    __mode = 'r'
    __file = None

    def __init__(self, file_path, mode=None, encoding='utf-8'):
        """
        'r'：以只读模式打开文件。如果文件不存在会抛出异常。
        'w'：以写入模式打开文件，会覆盖文件中原有的内容。如果文件不存在会创建一个新文件。
        'a'：以追加模式打开文件，不会覆盖原有的内容。如果文件不存在会创建一个新文件。
        'x'：以独占模式打开文件，只允许写入操作，如果文件已经存在会抛出异常。
        'b'：二进制模式，用于处理非文本文件，例如图片、视频等。
        't'：文本模式，用于处理文本文件，默认值。
         x+  而在 mode 参数中，如果包含 '+'，表示可以同时读写文件
        """
        self.__file_path = file_path
        if mode:
            self.__mode = mode
        self.__file = None

        self.encoding = encoding

    def __enter__(self):
        self.__file = open(self.file_path, self.mode)
        if not self.is_file():
            raise FileNotFoundError(f'No files matched, {self.file_path}')

        return self

    def __exit__(self, *exc_info):
        if self.file:
            self.file.close()

    @property
    def file_path(self):
        return self.__file_path

    @property
    def mode(self):
        return self.__mode

    @property
    def file(self):
        return self.__file

    @property
    def lines(self):
        with open(self.file_path, mode='r', encoding=self.encoding) as file:
            file_lines = sum(1 for line in file)
            return file_lines

    @property
    def dir(self):
        return os.path.dirname(os.path.abspath(self.file_path))

    @property
    def name(self):
        name, ext = os.path.splitext(os.path.basename(self.file_path))
        return name

    @property
    def ext(self):
        name, ext = os.path.splitext(os.path.basename(self.file_path))
        return ext

    @property
    def full_path(self):
        return f'{self.dir}/{self.name}{self.ext}'

    def is_file(self, file_path=None):
        if not os.path.exists(file_path or self.file_path):
            print(f"File does not exist: {file_path}")
            return False
        else:
            return True

    def copy(self, dst_path=None, file_suffix='_copy'):
        if self.is_file():
            if not dst_path:
                dst_path = self.dir
            current_file_full_path = self.full_path
            new_file_full_path = f'{dst_path}/{self.name}{file_suffix}{self.ext}'
            print(f'================> current_file_full_path: {current_file_full_path}')
            print(f'================> new_file_full_path: {new_file_full_path}')
            shutil.copy(current_file_full_path, new_file_full_path)

    def delete(self):
        if self.is_file():
            os.remove(self.file_path)

    def move(self, dst_path):
        if self.is_file():
            shutil.move(self.dir, dst_path)

    def get_content(self):
        if self.is_file():
            content = []
            with open(self.file_path, mode='r', encoding=self.encoding) as file:
                for line in file:
                    content.append(line)
            return content

    def write_content(self, content):
        with open(self.file_path, mode='w+', encoding=self.encoding) as file:
            for file_data in content:
                file.write(file_data)

    def append_content(self, content, has_return=True):
        with open(self.file_path, mode='a+', encoding=self.encoding) as file:
            str_content = str(content) + "\n" if has_return else str(content)
            print(f'================> str_content: {str_content}')
            file.write(str_content)

    def insert_line(self, line_number, content):
        input_data = str(content)
        input_data = input_data.replace("\'", "\"")
        file_content = self.get_content()
        if file_content:
            file_content.insert((line_number - 1), input_data + "\n")
            self.write_content(file_content)

    def append_line(self, line_number, content):
        input_data = str(content)
        input_data = input_data.replace("\'", "\"")
        file_content = self.get_content()
        if file_content:
            file_content.insert(line_number, input_data + "\n")
            self.write_content(file_content)

    def get_line(self, line_number):
        with open(self.file_path, mode='r', encoding=self.encoding) as file:
            if 1 <= line_number <= self.lines:
                return linecache.getline(self.file_path, line_number)

    def delete_line(self, line_number):
        file_content = self.get_content()
        if file_content:
            del file_content[(line_number - 1)]
            self.write_content(file_content)

    def update_line(self, line_number, content):
        input_data = str(content)
        input_data = input_data.replace("\'", "\'")
        content = self.get_content()
        if content:
            # 修改方法
            content[(line_number - 1)] = input_data + "\n"
            with open(self.file_path, mode='w+', encoding=self.encoding) as file:
                for file_data in content:
                    file.write(file_data)

    def find(self, search_text):
        with open(self.file_path, mode='r', encoding=self.encoding) as file:
            result = []
            for line_num, line in enumerate(file, 1):
                for match in re.finditer(search_text, line):
                    print(f"Line {line_num}: {match.start()} - {match.end()}: {line.strip()}")
                    result.append(line_num)
            return result

    def replace(self, regexp, new_char, callback=None):
        """
        r'regexp'       # 默认贪婪匹配
        r'regexp?'      # 非贪婪匹配
        """
        with open(self.file_path, mode='r+', encoding=self.encoding) as file:
            content = file.read()
            content = re.sub(regexp, new_char, content)
            if hasattr(callback, '__call__'):
                print(f'================> callback: {callback}')
                callback(content)
            file.seek(0)
            file.write(content)
            file.truncate()

    def clear_space(self):
        self.replace(r' ', '')

    def clear_return(self):
        self.replace(r"\n", "")


if __name__ == '__main__':
    path = './demo.txt'

    with FileHandle(path) as f:
        file_dir = f.dir
        print(f'================> file_dir: {file_dir}')
        file_name = f.name
        print(f'================> file_name: {file_name}')
        file_ext = f.ext
        print(f'================> file_ext: {file_ext}')
        full_path = f.full_path
        print(f'================> full_path: {full_path}')
