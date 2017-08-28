# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_pymongo import PyMongo


login_manager = LoginManager()
# login_manager.login_view = 'logins.login'

cors = CORS()
db = SQLAlchemy()
mongo = PyMongo()
