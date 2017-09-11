# -*- coding: utf-8 -*-
from api import create_app
from utils.ext import login_manager
from api.authentication.model import Permission, User, Role, Groups
from api.authentication.url import get_auth_resources
from flask import Blueprint, jsonify, request, make_response, session, render_template
from api.authentication.view import module
from os import environ

config_name = environ.get("FLASK_CONFIG", 'Devops')
app = create_app('config.settings.{0}'.format(config_name))

# 蓝图功能, 注册api url
app.register_blueprint(get_auth_resources(), url_prefix='/api/v1')
app.register_blueprint(module)

home_page = Blueprint('home', __name__, template_folder='./vue-init/dist', static_folder='./vue-init/dist/static')


@home_page.route('/')
def home():
    return render_template('index.html')

app.register_blueprint(home_page)


@app.route("/test")
def hello():
    from flask_login import current_user
    # print(current_user.is_authenticated, current_user.__dict__)
    # print(request.url, request.cookies, request.headers.__dict__)
    # print('ticket: ', request.args.get("ticket", None))
    # response = make_response("test")
    # response.set_cookie("name", "xxx")
    # print(response)
    # print(session.items(), session.get('user_id'))
    # return render_template('index.html')
    return render_template('auth.html', name='lf')
    # return "Hello World from Flask"


# start


@login_manager.user_loader
def load_user(user_id):
    """@login_required 获取用户信息"""
    user = User.query.get(user_id)
    # print("user login:", user)
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return {"err": "not login"}
    # return render_template('auth.html', name='lf')

# end


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082)
