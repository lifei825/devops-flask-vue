# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api
from .view import Auth, Users, UserQuery


def get_auth_resources():
    auth_bp = Blueprint('auth', __name__, template_folder='../../templates', static_url_path='', static_folder='')

    api = Api(auth_bp)

    api.add_resource(Auth, '/login')
    api.add_resource(Users, '/user')
    api.add_resource(UserQuery, '/user/<nt_account>')

    return auth_bp





