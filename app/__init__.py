from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# import models
# from models import User

app = Flask(__name__, template_folder='../views')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sql'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)
