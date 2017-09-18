# -*- coding: utf-8 -*-
""" manage.py runserver -h 127.0.0.1 -p 8888 --debug """
from api import create_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import render_template, jsonify, request, make_response, session
from utils.ext import db
from utils.permission import user_datastore
from api.authentication.model import Permission, User, Role, Groups
from utils.ext import login_manager
from api.authentication.url import get_auth_resources
from api.authentication.view import module
from os import environ


config_name = environ.get("FLASK_CONFIG", 'Devops')
app = create_app(config_name)

# 蓝图功能, 注册api url
app.register_blueprint(get_auth_resources(), url_prefix='/api/v1')
app.register_blueprint(module)

manager = Manager(app)
migrate = Migrate(app, db)

# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade
manager.add_command('db', MigrateCommand)


@manager.command
def create_user():
    # db.drop_all()
    db.create_all()

    g1 = Groups(name="test")
    g2 = Groups(name="admin")
    db.session.add(g1)
    db.session.add(g2)
    db.session.commit()
    db.session.close()

    for permissions, (name, desc) in Permission.PERMISSION_MAP.items():
        user_datastore.find_or_create_role(name=name,
                                           description=desc,
                                           permissions=permissions,
                                           groups=Groups.query.filter_by(name="admin").first()
                                           )

    for email, username, passwd, permissions in (
            ('lifei', 'lifei', '123', (Permission.LOGIN, Permission.EDITOR)),
            ('admin', 'admin', 'admin123_2017', (Permission.ADMIN,))
    ):
        user_datastore.create_user(email=email, username=username, password=passwd)
        for permission in permissions:
            user_datastore.add_role_to_user(email, Permission.PERMISSION_MAP[permission][0])
    db.session.commit()

# start


@login_manager.user_loader
def load_user(user_id):
    """@login_required 获取用户信息"""
    user = User.query.get(user_id)
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return {"err": "not login"}
    # return render_template('auth.html', name='lf')

# end


@manager.app.route('/')
def h():
    print(request.url, request.cookies, request.headers.__dict__)
    print('ticket: ', request.args.get("ticket", None))
    response = make_response("test")
    response.set_cookie("name", "xxx")
    print(response)
    print(session.items(), session.get('user_id'))
    return render_template('game.html', name='lf')
    # return {'say': "hello world"}, 250, [('HHHH', '111100000')]


@manager.app.route('/logout')
def logout():
    from flask_security import logout_user
    logout_user()
    return "logout ok"


@manager.app.route('/check')
def check():
    import requests, re
    from flask_security import login_user
    ticket = request.args.get("ticket", None)
    a = requests.get("https://sso.asiainfo.com/serviceValidate", params={
        'ticket': ticket,
        'service': 'http://localhost:8080'})
    print("go to check", ticket, a.text)
    # username = re.findall(a.text, "")

    user = User.query.filter_by(email='admin').first()
    a = login_user(user)
    return jsonify({"tocken": 123, "user": "admin"})

if __name__ == '__main__':
    # python manage.py  runserver -h 0.0.0.0 -p 8888
    manager.run()
