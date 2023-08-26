FROM --platform=linux/amd64 python:3.8.16

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .
RUN chmod a+x boot.sh

EXPOSE 8181

CMD ["./boot.sh"]