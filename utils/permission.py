# -*- coding: utf-8 -*-
from api.authentication.model import Role, User, Permission
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
from flask_jwt import current_identity

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore, register_form=LoginForm)

# 权限装饰器


def permission_required(permission, active=True):
    def decorator(f):
        @wraps(f)
        def _deco(self, *args, **kwargs):
            print("self post", dict(request.values.items()))
            self.gid = request.values.get("gid", 2)

            if permission == Permission.SUPER_ADMIN:
                self.gid = 2

            else:
                self.gid = int(self.gid) if self.gid else 2

            uid = current_identity.__dict__.get('id')
            self.user = User.query.get(int(uid))

            if not self.user.can(self.gid, abs(permission)) and active:
                print("permission 403")
                abort(403)
            elif request.method != 'GET':
                # 审计
                print('{0}通过{1}方法,访问{2}, 参数: {3}'.format(self.user.username,
                                                         request.method,
                                                         request.path,
                                                         dict(request.values.items())
                                                         ))

            return f(self, *args, **kwargs)
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
    user = User.query.filter_by(email=username).first()
    if user and user.verify_password(password):
        if user.active:
            return user


# jwt 获取身份
def identity(payload):
    user_id = int(payload['identity'])
    return User.query.get(user_id)
