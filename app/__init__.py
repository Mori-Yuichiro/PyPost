from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# import models
# from models import User

app = Flask(__name__, template_folder='../views')

login_manager = LoginManager(app)
login_manager.init_app(app)
# ログインしていない状態でログインが必要なページにアクセスした時に、リダイレクトするページを指定
login_manager.login_view = 'index'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sql'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)
