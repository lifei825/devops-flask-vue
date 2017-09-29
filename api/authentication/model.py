from flask_security import RoleMixin, UserMixin
from utils.ext import db
from functools import reduce
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


class Permission(object):
    LOGIN = 0X01
    EDITOR = 0x02
    OPERATOR = 0x04
    ADMIN = 0xff        # hex(255)
    SUPER_ADMIN = -0xff
    PERMISSION_MAP = {
        LOGIN: ('login', 'Login user'),
        EDITOR: ('editor', 'Editor'),
        OPERATOR: ('op', 'Operator'),
        ADMIN: ('admin', 'administrator'),
    }

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    permissions = db.Column(db.Integer, default=Permission.LOGIN)
    description = db.Column(db.String(255))
    groups_id = db.Column(db.Integer, db.ForeignKey('groups.id'))


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime(), default=datetime.now())
    roles = db.relationship('Role', backref='groups', lazy='dynamic')

    def to_json(self):
        doc = self.__dict__
        if "_sa_instance_state" in doc:
            del doc["_sa_instance_state"]

        if doc.get('confirmed_at', None):
            doc['confirmed_at'] = doc['confirmed_at'].strftime('%F %T')

        return doc


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    job = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime(), default=datetime.now())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    last_login_at = db.Column(db.String(255))
    current_login_at = db.Column(db.String(255))
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)

    # 权限验证
    def can(self, gid, permissions=Permission.LOGIN):
        if self.roles is None:
            print("can false")
            return False
        # 判断是否在组中 [ r for r in self.roles if 组 == r.组]
        permissions_list = [r.permissions for r in self.roles if r.groups_id == int(gid) or r.groups_id == 2]
        if permissions_list:
            all_perms = reduce(lambda x, y: x | y, permissions_list)
        else:
            all_perms = 0

        return all_perms & permissions == permissions

    def can_admin(self):
        return self.can(gid=1, permissions=Permission.ADMIN)

    # password不可读
    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    # password加密
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


