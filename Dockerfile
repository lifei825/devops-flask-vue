# https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/tags/
FROM  tiangolo/uwsgi-nginx-flask:flask-python3.5-index

ENV C_FORCE_ROOT true

# Set the default timezone to Shanghai
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime; \
    echo "Asia/Shanghai" > /etc/timezone; \
    dpkg-reconfigure -f noninteractive tzdata

COPY . /app/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
#COPY ./config/supervisor_celery.conf /etc/supervisor/conf.d/
RUN pip install --upgrade pip ; pip install -r requirements.txt -i https://pypi.doubanio.com/simple

ENTRYPOINT ["/entrypoint.sh"]

WORKDIR /app

CMD ["/usr/bin/supervisord"]