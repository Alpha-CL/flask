from urllib.parse import urlparse, quote, unquote, urlencode, quote_plus, unquote_plus, urlunparse


class URL(object):
    @classmethod
    def encode(cls, target, encoding=None, plus=False):
        """
        quote('a&b/c')          # 未编码斜线
        quote_plus('a&b/c')     # 编码了斜线
        """
        return quote(target, encoding=encoding) if plus else quote_plus(target, encoding=encoding)

    @classmethod
    def decode(cls, target, encoding='utf-8', plus=False):
        """
        parse.unquote('1+2')    # 不解码加号
        unquote_plus('1+2')     # 把加号解码为空格
        """
        return unquote(target, encoding=encoding) if plus else unquote_plus(target, encoding=encoding)


class ParseUrl(URL):
    demo_url = 'https://user:pwd@domain:80/path;params?query=queryarg#fragment'

    __parse_result = None
    __scheme = None
    __netloc = None
    __path = None
    __params = None
    __query = None
    __fragment = None

    def __init__(self, url=None):
        self.__parse_result = urlparse(url or self.demo_url)
        scheme, netloc, path, params, query, fragment = self.__parse_result
        self.__scheme = scheme
        self.__netloc = netloc
        self.__path = path
        self.__params = params
        self.__query = query
        self.__fragment = fragment

    @property
    def result(self):
        return self.__parse_result

    # 协议
    @property
    def scheme(self):
        return self.__scheme

    # 域名
    @property
    def domain(self):
        return self.__netloc

    # 分层路径
    @property
    def path(self):
        return self.__path

    # path 后的参数
    @property
    def params(self):
        return self.__params

    # ? 后的参数
    @property
    def query(self):
        return self.__query

    @property
    def hash(self):
        return self.__fragment

    @property
    def hostname(self):
        return self.result.hostname

    @property
    def port(self):
        return self.result.port

    @property
    def username(self):
        return self.result.username

    @property
    def password(self):
        return self.result.password

    @classmethod
    def create_query(cls, query_dict, encoding='utf-8'):
        return urlencode(query_dict).encode(encoding)


class CreateUrl(URL):
    __url = None

    __parse_result = None
    __scheme = None
    __netloc = None
    __path = None
    __params = None
    __query = None
    __fragment = None

    __hostname = None
    __port = None
    __username = None
    __password = None

    def __init__(
            self,
            scheme=None,
            netloc='',
            path=None,
            params=None,
            query=None,
            fragment=None,
            hostname=None,
            port=None,
            username=None,
            password=None
    ):
        self.__scheme = scheme or 'http'
        self.__netloc = netloc
        self.__path = path or ''
        self.__params = params
        self.__query = query
        self.__fragment = fragment

        if username:
            self.__netloc = '{}@{}'.format(username, netloc)
        else:
            self.__netloc = netloc

        if password:
            if username:
                self.__netloc = '{}:{}@{}'.format(username, password, netloc)
            else:
                self.__netloc = ':{}@{}'.format(password, netloc)

        if hostname:
            if self.__netloc:
                self.__netloc = '{}.{}'.format(self.__netloc, hostname)
            else:
                self.__netloc = hostname

        if port:
            self.__netloc = '{}:{}'.format(self.__netloc, port)

        self.__url = self.create()

    def create(self):

        url_parts = {
            "scheme": self.__scheme,
            "netloc": self.__netloc,
            "path": self.__path,
            "params": self.__params,
            "query": self.__query,
            "fragment": self.__fragment,
        }

        print(f'================> url_parts: {url_parts}')

        self.__url = urlunparse(tuple(url_parts.values()))
        return self.__url

    @property
    def url(self):
        return self.__url


if __name__ == '__main__':
    p_url = ParseUrl().result
    print(f'================> p_url: {p_url}')

    c_url = CreateUrl(
        hostname='0.0.0.0',
        port='80',
        path='/api',
        params='a=b',
        query='query',
        fragment='fragment',
        username='user',
        password='pwd'
    ).url
    print(f'================> c_url: {c_url}')
