# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from flask import flash, redirect, Blueprint, current_app
from flask_security import login_required, login_user, logout_user
from .model import User, Permission, Groups, Role
from utils.permission import permission_required
from utils.ext import db
from flask_login import current_user
import json
import logging
from utils.ErrorCode import *
import jwt
from flask_jwt import jwt_required, current_identity
from utils.helper import Argument
from sqlalchemy import and_, or_


module = Blueprint('logout', __name__)


@module.route('/logout')
def logout():
    logout_user()
    return "logout ok"


class Auth(Resource):
    def __init__(self):
        super(Auth, self).__init__()

    @jwt_required()
    def put(self):
        """
        token验证
        ---
        tags:
        - LOGIN
        parameters:
          - in: header
            name: Authorization
            type: string
            required: true
            description: "JWT <token>"
        responses:
          200:
            description: token验证
            schema:
              properties:
                result:
                  type: string
                  default: ok
            examples:
                {
                    "result": {
                        "verify": True,
                    },
                    "state": "ok"
                }
        """

        return {'result': {'verify': True}, 'state': 'ok'}, 200

    def post(self):
        """
        用户登录
        ---
        tags:
        - LOGIN
        parameters:
          - in: formData
            name: email
            type: string
            description: "邮箱"
          - in: formData
            name: password
            type: string
            description: "密码"
        responses:
          200:
            description: 用户认证登录
            schema:
              properties:
                result:
                  type: string
                  default: ok
            examples:
                {
                    "result": {
                        "exp": 1498621139,
                        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI",
                        "username": "lifei5"
                    },
                    "state": "ok"
                }
        """
        email = None
        token = None
        exp = None
        state = STATE_OK
        try:
            email = request.values.get('email', None)
            password = request.values.get('password', None)
            _secret = current_app.config.get('SECRET_KEY')
            print("identfied", email, password)

            with current_app.test_client() as c:
                resp = c.post('/auth', headers={'Content-Type': 'application/json'},
                              data=json.dumps({"username": email, "password": password}))
                data = json.loads(resp.data.decode('utf8'))
                print("auth", data)
                if data.get('error'):
                    raise ErrorCode(451, data.get('description', "Bad Request"))

            token = data.get('access_token', None)
            exp = jwt.decode(token, key=_secret).get("exp")

            uid = jwt.decode(token, key=_secret).get("identity")
            user = User.query.get(int(uid))
            login_user(user)

        except Exception as e:
            logging.error("get token error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))

        return {'result': {'username': email,
                           'token': token,
                           'exp': exp,
                           'permission': Permission.PERMISSION_MAP}, 'state': state.message}, state.eid


class Users(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user', type=str, required=True, location='form')
        self.parser.add_argument('passwd', type=str, required=True, location='form')

        self.parser_post = reqparse.RequestParser()
        self.parser_post.add_argument('roles', type=list, action='append', location=['form', 'values', 'json'])

        self.parser_get = reqparse.RequestParser()
        self.parser_get.add_argument('user', type=str, required=False, location='args')
        super(Users, self).__init__()

    @jwt_required()
    @permission_required(Permission.VIEW)
    def get(self):
        """
            员工列表接口
            ---
            tags:
            - USER
            parameters:
              - in: header
                name: Authorization
                type: string
                required: true
                description: "JWT <token>"
              - in: query
                name: gid
                type: integer
              - in: query
                name: page
                type: integer
                description: 当前页
              - in: query
                name: pageSize
                type: integer
                description: 每页显示量
            responses:
              200:
                description: 仅管理员可访问
        """
        doc = []
        state = STATE_OK
        users_total = 0

        try:
            page = int(request.values.get('page', 1))
            page_size = int(request.values.get('pageSize', 10))
            keyword = request.values.get('keyword', "")

            # 如果是超级管理员可获取所有用户信息
            if self.gid == 0:
                users_class = User.query.filter(or_(User.username.like("%"+keyword+"%"),
                                                    User.email.like("%"+keyword+"%"),
                                                    User.phone.like("%"+keyword+"%"),
                                                    User.job.like("%"+keyword+"%"),)
                                                ).order_by(User.id.desc()).paginate(page, page_size, error_out=True)

            # 否则获取指定项目下的所有用户
            else:
                users_class = User.query.join(User.roles).filter(
                    and_(Role.groups_id == self.gid,
                         or_(User.email.like("%"+keyword+"%"),
                             User.phone.like("%"+keyword+"%"),
                             User.username.like("%"+keyword+"%"),
                             User.job.like("%"+keyword+"%"),))
                ).order_by(User.id.desc()).paginate(page, page_size, error_out=False)

            users = users_class.items
            users_total = users_class.total

            doc = [u.to_json(self.gid) for u in users]

        except Exception as e:
            logging.error("get user info error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(1, "unknown error:" + str(e))

        return {'result': {'doc': doc, 'total': users_total}, 'state': state.message}, state.eid

    @jwt_required()
    @permission_required(Permission.VIEW)
    def post(self):
        """
            用户添加修改
            ---
            tags:
            - USER
            parameters:
              - in: header
                name: Authorization
                type: string
                required: true
                description: "JWT <token>"
              - in: formData
                name: id
                type: integer
                description: "用户ID"
              - in: formData
                name: username
                type: string
                description: "用户名"
              - in: formData
                name: job
                type: string
                description: "职位"
              - in: formData
                name: phone
                type: string
                description: "手机"
              - in: formData
                name: email
                type: string
                description: "邮箱"
              - in: formData
                name: active
                type: string
                description: "是否激活"
              - in: formData
                name: roles
                type: array
                description: "角色"
            responses:
              200:
                description: 员工信息修改接口
        """

        state = STATE_OK
        rs = False
        try:
            request_param = dict(request.values.items())
            print("user post:", request_param)
            uid = request.values.get("id", None)
            username = request.values.get("username", None)
            phone = request.values.get("phone", None)
            email = request.values.get("email", None)
            job = request.values.get("job", None)
            roles = request.values.get("roles", "").split(',')
            print(roles, type(roles))

            if not username and not email:
                raise STATE_PARAM_ERR

            if not uid:
                user = User(username=username,
                            email=email,
                            phone=phone,
                            job=job,
                            active=True)

                password = current_app.config.get('PASSWORD_KEY')
                user.password = password

            else:
                user = User.query.get(int(uid))
                user.username = username,
                user.email = email,
                user.phone = phone,
                user.job = job
                user.active = True

            if roles:
                print("roles", roles)
                for r in roles:
                    role = Role.query.filter_by(groups_id=self.gid, permissions=int(r)).first()
                    print("role s", role)
                    if role not in user.roles:
                        print("not role s")
                        user.roles.append(role)

                # user.roles
            print("db sssss")
            db.session.add(user)
            db.session.commit()

            rs = True

        except Exception as e:
            logging.error("get user info error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(1, "unknown error:" + str(e))

        return {'result': rs, 'state': state.message}, state.eid


class Group(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(argument_class=Argument)
        self.parser.add_argument('id', type=int, required=False, location=['form', 'values'])
        self.parser.add_argument('name', type=str, required=True, location=['form', 'values'], nullable=False, trim=True)
        self.parser.add_argument('description', type=str, required=False, location=['form', 'values'], trim=True)
        super(Group, self).__init__()

    @jwt_required()
    @permission_required(Permission.VIEW, active=False)
    def get(self):
        """
            查询项目列表
            ---
            tags:
            - GROUP
            parameters:
              - in: header
                name: Authorization
                type: string
                required: true
                description: "JWT <token>"
              - in: query
                name: gid
                type: string
              - in: query
                name: page
                type: string
                description: 当前页
              - in: query
                name: pageSize
                type: string
                description: 每页显示量
            responses:
              200:
                description: 员工信息查询接口
        """
        doc = []
        state = STATE_OK
        groups_total = 0

        try:
            page = int(request.values.get('page', 1))
            page_size = int(request.values.get('pageSize', 10))
            keyword = request.values.get('keyword', "")

            if self.gid == 2 and [r for r in self.user.roles if r.groups_id == 2]:
                groups_class = Groups.query.filter(Groups.name.like('%{0}%'.format(keyword))).order_by(
                    Groups.id.desc()).paginate(page, page_size, error_out=False)

            else:
                groups_class = Groups.query.join(Role.groups).filter(
                    and_(Groups.id.in_((r.groups_id for r in self.user.roles)),
                         Groups.name.like("%"+keyword+"%"))).order_by(
                    Groups.id.desc()).paginate(page, page_size, error_out=False)

            groups = groups_class.items
            groups_total = groups_class.total
            doc = [g.to_json() for g in set(groups)]

            print('send doc', doc)

        except Exception as e:
            logging.error("get user info error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))

        return {'result': {'doc': doc, 'total': groups_total}, 'state': state.message}, state.eid

    @jwt_required()
    @permission_required(Permission.SUPER_ADMIN)
    def post(self):
        """
            项目添加
            ---
            tags:
            - GROUP
            parameters:
              - in: header
                name: Authorization
                type: string
                required: true
                description: "JWT <token>"
              - in: formData
                name: id
                type: string
                description: "项目id"
              - in: formData
                name: name
                type: string
                required: true
                description: "项目名称"
              - in: formData
                name: description
                type: string
                description: "项目描述"
            responses:
              200:
                description: 项目添加
        """
        state = STATE_OK
        rs = True

        try:
            print("start post group")
            data = self.parser.parse_args()
            gid = data.get("id", None)
            name = data.get("name", None)
            description = data.get("description", None)
            if not name:
                raise STATE_PreconditionFailed

            print("post all:", request.values.__dict__, name, description, type(gid))

            if gid:
                group = Groups.query.get(gid)
                group.name = name
                group.description = description

                db.session.add(group)
                db.session.commit()

            else:
                group = Groups(name=name, description=description)
                db.session.add(group)

                for permissions, (role, desc) in Permission.PERMISSION_MAP.items():
                    r = Role(name=role, description=desc, permissions=permissions, groups=group)
                    db.session.add(r)

                db.session.commit()

        except Exception as e:
            rs = False
            logging.error("get user info error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))

        return {'result': rs, 'state': state.message}, state.eid

    @jwt_required()
    @permission_required(Permission.SUPER_ADMIN)
    def delete(self):
        """
            项目添加
            ---
            tags:
            - GROUP
            parameters:
              - in: header
                name: Authorization
                type: string
                required: true
                description: "JWT <token>"
              - in: formData
                name: id
                type: string
                description: "项目id"
            responses:
              200:
                description: 项目添加
        """
        state = STATE_OK
        rs = True

        try:
            gid = int(request.values.get('id'))
            if gid == 2:
                raise ErrorCode(501, "无法删除超级管理组")

            group = Groups.query.get(gid)

            db.session.query(Role).filter(or_(Role.groups_id == gid, Role.groups_id == None)).delete()
            db.session.delete(group)
            db.session.commit()

        except Exception as e:
            rs = False
            logging.error("get user info error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))

        return {'result': rs, 'state': state.message}, state.eid
