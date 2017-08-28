# -*- coding: utf-8 -*-
from api.authentication.model import Role, User
from flask_security import SQLAlchemyUserDatastore, Security, login_user
from functools import wraps
from flask_login import current_user
from flask import abort, request, redirect, current_app
from .ext import db
import requests
import re
from flask_security.forms import LoginForm
import logging
from utils.ErrorCode import *

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore, register_form=LoginForm)

# 权限装饰器


def permisson_required(permission):
    def decorator(f):
        @wraps(f)
        def _deco(*args, **kwargs):
            print("self post", dict(request.values.items()))
            gid = request.values.get("gid", None)
            print("gid:", gid)
            print("is auth:", current_user.is_authenticated)
            # print("is active:", current_user.is_active, current_user.email)

            if current_user.is_anonymous:
                print("is anonymous")
                abort(403)

            if not current_user.can(gid, permission):
                print("permission 403")
                abort(403)
            return f(*args, **kwargs)
        return _deco
    return decorator


def sso_required(f):
    @wraps(f)
    def _deco(*args, **kwargs):
        try:
            # 若不是登录状态 跳转到http://sso.asiainfo.com/验证
            print("user info: ", current_user.__dict__)
            ticket = request.args.get("ticket", None)
            service = request.args.get("service", request.url.split('?')[0])
            if ticket:
                # 有ticket拿着去公司api验证 获取用户名, service的url必须和请求的url一致

                rs = requests.get("https://sso.asiainfo.com/serviceValidate", params={
                    'ticket': ticket,
                    'service': service})

                print("go to check", ticket, rs.text)
                username = re.findall("""<cas:user>(.*?)</cas:user>""", rs.text)
                if username:
                    user = User.query.filter_by(username=username[0]).first()
                    password = current_app.config.get('PASSWORD_KEY')
                    if not user:
                        user = User(username=username[0], active=1)
                        user.password = password
                        db.session.add(user)
                        db.session.commit()

                        from task.tasks import sync_employee_to_mysql
                        sync_employee_to_mysql.delay(username[0])

                    elif not user.verify_password(password):
                        user.password = password
                        db.session.add(user)
                        db.session.commit()

                    s = login_user(user)
                    if not s:
                        raise STATE_LOGIN_ERR

                else:
                    raise STATE_LOGIN_ERR

            else:

                return redirect("https://sso.asiainfo.com/login?service=%s" % request.url, code=301)

        except Exception as e:
            logging.error("sso verify error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(1, "unknown error:" + str(e))

            return {'result': 'sso verify error', 'state': state.message}, state.eid

        return f(*args, **kwargs)

    return _deco


# jwt 验证用户名密码
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return user


# jwt 获取身份
def identity(payload):
    user_id = int(payload['identity'])
    return User.query.get(user_id)
