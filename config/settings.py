# -*- coding: utf-8 -*-
from datetime import timedelta


class Config(object):
    DEBUG = True

    SECRET_KEY = 'key-110-password'

    PASSWORD_KEY = "password"  # 统一用户登录密码

    SESSION_COOKIE_DOMAIN = 'feifeiwd.com'

    # cook保存到redis过期时间
    # PERMANENT_SESSION_LIFETIME = timedelta(seconds=600)
    JWT_EXPIRATION_DELTA = timedelta(seconds=60 * 60 * 24 * 10)

    # SESSION_STORE = {'host': 'paas-test.asiainfo.com', 'port': 30487, 'db': 2, 'password': '7788'}

    SWAGGER = {'title': 'Devops API', 'uiversion': 2, 'description': ''}


class Devops(Config):

    SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1:3306/backend?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # celery config
    BROKER_URL = 'redis://:123@127.0.0.1:6379/7'
    CELERY_RESULT_BACKEND = 'redis://:123@127.0.0.1:6379/8'

    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
    CELERY_ACCEPT_CONTENT = ['json']
    CELERYD_MAX_TASKS_PER_CHILD = 40  # 每个worker执行了多少任务就会死掉

    CELERYBEAT_SCHEDULE = {
        'add-every-1-minutes-active': {
            'task': 'task.tasks.some',
            'schedule': timedelta(seconds=60),
        },
    }


class DevopsProduction(Config):

    SQLALCHEMY_DATABASE_URI = 'mysql://root:passwd@mysql:3306/backend?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # celery config
    BROKER_URL = 'redis://redis:6379/13'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/14   '
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
    CELERY_ACCEPT_CONTENT = ['json']
    CELERYD_MAX_TASKS_PER_CHILD = 40  # 每个worker执行了多少任务就会死掉

    CELERYBEAT_SCHEDULE = {
        'add-every-1-minutes-active': {
            'task': 'task.tasks.maintain_monitor_active',
            'schedule': timedelta(seconds=60),
        },
    }

