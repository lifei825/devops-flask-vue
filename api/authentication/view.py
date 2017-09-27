# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from flask import flash, redirect, Blueprint, current_app
from flask_security import login_required, login_user, logout_user
from .model import User, Permission, Groups, Role
from utils.permission import permisson_required
from utils.ext import db
from flask_login import current_user
import json
import logging
from utils.ErrorCode import *
import jwt
from flask_jwt import jwt_required, current_identity
from utils.helper import Argument


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

            with current_app.test_client() as c:
                resp = c.post('/auth', headers={'Content-Type': 'application/json'},
                              data=json.dumps({"username": email, "password": password}))
                data = json.loads(resp.data.decode('utf8'))
                if data.get('error'):
                    raise ErrorCode(451, data.get('description', "Bad Request"))

            token = data.get('access_token', None)
            exp = jwt.decode(token, key=_secret).get("exp")

        except Exception as e:
            logging.error("get token error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))

        return {'result': {'username': email, 'token': token, 'exp': exp}, 'state': state.message}, state.eid


class Users(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user', type=str, required=True, location='form')
        self.parser.add_argument('passwd', type=str, required=True, location='form')

        self.parser_get = reqparse.RequestParser()
        self.parser_get.add_argument('user', type=str, required=False, location='args')
        super(Users, self).__init__()

    @jwt_required()
    def get(self):
        """
            员工信息查询接口
            ---
            tags:
            - USER
            parameters:
              - in: header
                name: Authorization
                type: string
                required: true
                description: "JWT <token>"
            responses:
              200:
                description: 员工信息查询接口
        """
        doc = {}
        state = STATE_OK

        try:
            doc = current_identity.__dict__
            del doc['password_hash']
            del doc['_sa_instance_state']
            del doc['confirmed_at']

        except Exception as e:
            logging.error("get user info error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(1, "unknown error:" + str(e))

        return {'result': doc, 'state': state.message}, state.eid

    @jwt_required()
    def post(self):
        """
            员工信息修改接口
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
                name: phone
                type: string
                description: "手机"
              - in: formData
                name: email
                type: string
                description: "邮箱"
            responses:
              200:
                description: 员工信息修改接口
        """

        state = STATE_OK
        rs = False
        try:
            uid = current_identity.__dict__.get('id')
            phone = request.values.get("phone", None)
            email = request.values.get("email", None)
            user = User.query.get(int(uid))
            if phone or email:
                if phone:
                    user.phone = phone

                if email:
                    user.email = email

                db.session.add(user)
                db.session.commit()

                rs = True

            else:
                raise STATE_PARAM_ERR

        except Exception as e:
            logging.error("get user info error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(1, "unknown error:" + str(e))

        return {'result': rs, 'state': state.message}, state.eid


class UserQuery(Resource):
    def __init__(self):
        super(UserQuery, self).__init__()

    def get(self, nt_account):
        """
            指定账户员工信息查询接口
            ---
            tags:
            - USER
            parameters:
              - in: path
                name: nt_account
                type: string
                required: true
                description: "nt_account "
            responses:
              200:
                description: 指定员工信息查询接口
        """
        doc = {}
        state = STATE_OK

        try:
            user = User.query.filter_by(username=nt_account).first()
            if not user:
                raise STATE_EmptyData_ERR

            doc.update({'email': user.email, 'phone': user.phone})

        except Exception as e:
            logging.error("get user info error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(1, "unknown error:" + str(e))

        return {'result': doc, 'state': state.message}, state.eid


class Group(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(argument_class=Argument)
        self.parser.add_argument('id', type=int, required=False, location=['form', 'values'])
        self.parser.add_argument('name', type=str, required=True, location=['form', 'values'], nullable=False, trim=True)
        self.parser.add_argument('description', type=str, required=False, location=['form', 'values'], trim=True)
        super(Group, self).__init__()

    @jwt_required()
    @permisson_required(Permission.LOGIN)
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

            is_super_admin = [r.__dict__ for r in self.user.roles if r.groups_id == 2]
            if is_super_admin:
                groups_class = Groups.query.filter_by().order_by(Groups.id.desc()).paginate(
                    page, page_size, error_out=False)
                groups = groups_class.items
                groups_total = groups_class.total

            else:
                groups = [role.groups for role in self.user.roles][(page-1)*page_size:page*page_size]
                groups_total = len(groups)

            doc = [g.to_json() for g in set(groups)]

            print('send doc', doc)

        except Exception as e:
            logging.error("get user info error: %s." % str(e))
            state = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))

        return {'result': {'doc': doc, 'total': groups_total}, 'state': state.message}, state.eid

    @jwt_required()
    @permisson_required(Permission.LOGIN)
    # @permisson_required(Permission.SUPER_ADMIN)
    def post(self):
        """
            项目添加
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
            name = data.get("name", "no name")
            description = data.get("description", None)
            print("name:", name)
            if not name:
                print("not name")

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

