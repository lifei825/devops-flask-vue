# -*- coding: utf-8 -*-
from flask import Flask, flash, request
from .authentication.url import get_auth_resources
from utils.ext import db, cors, mongo
from utils.permission import security, authenticate, identity
from flask_kvsession import KVSessionExtension
import redis
from simplekv.memory.redisstore import RedisStore
from flask_login import user_logged_in, user_logged_out
import datetime
from flasgger import Swagger
from flask_jwt import JWT


def create_app(config_name, template_folder=None, static_folder=None):
    app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
    app.config.from_object(config_name)

    # jwt初始化
    jwt = JWT(app, authenticate, identity)
    jwt.init_app(app)

    # session信息save到reidis
    # session = KVSessionExtension()
    # store = RedisStore(redis.StrictRedis(**app.config['SESSION_STORE']))
    # session.init_app(app, store)
    # session.cleanup_sessions(app)

    # 解决跨域
    cors.init_app(app, allow_headers='*')

    # mysql init
    db.init_app(app)

    # mongodb init
    # mongo.init_app(app)

    # 权限管理
    security.init_app(app)

    # 信号
    add_signals(app)

    # 临时激活一个请求环境。在这个 环境中可以像以视图函数中一样操作 request 、g 和 session 对象
    with app.test_request_context():
        db.create_all()

    # 蓝图功能, 注册api url
    # app.register_blueprint(get_auth_resources(), url_prefix='/api')
    # app.register_blueprint(get_cmdb_resources(), url_prefix='/api/v1')

    # login 管理
    from utils.ext import login_manager
    import datetime
    login_manager.remember_cookie_duration = datetime.timedelta(seconds=60)
    login_manager.init_app(app)

    # api文档初始化
    Swagger(app)

    return app


def add_signals(app):
    """Attaches the user_logged_in and user_logged_out signals to app. Here, we
    just use it to flash messages.
    """
    @user_logged_in.connect_via(app)
    def logged_in(sender, user, **extra):
        if 'X-Forwarded-For' in request.headers:
            remote_addr = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1]
        else:
            remote_addr = request.remote_addr or 'untrackable'

        old_current_login, new_current_login = user.current_login_at, datetime.datetime.now()
        old_current_ip, new_current_ip = user.current_login_ip, remote_addr

        user.last_login_at = old_current_login or new_current_login
        user.current_login_at = new_current_login
        user.last_login_ip = old_current_ip or new_current_ip
        user.current_login_ip = new_current_ip
        user.login_count = user.login_count + 1 if user.login_count else 1
        db.session.add(user)
        db.session.commit()
        flash('You were Login Success. %s ' % datetime.datetime.now())

    @user_logged_out.connect_via(app)
    def logged_out(app, user):
        flash('You were logged out. %s ' % datetime.datetime.now())
        return
