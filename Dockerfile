FROM python:3.6.9-alpine

WORKDIR /

EXPOSE 8000

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --no-cache gcc make libc-dev linux-headers pcre-dev && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask prometheus_client py_eureka_client uwsgi

COPY app.py /app.py

CMD uwsgi --http-socket 0.0.0.0:8000 --wsgi-file app.py --callable app_dispatch --processes 4 --threads 2 --stats 0.0.0.0:9000 --uid nobody --gid nobody
