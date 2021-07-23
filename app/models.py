from enum import unique
from flask_login import UserMixin
from sqlalchemy.orm import backref

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#user情報用のクラス
class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    password = db.Column(db.String(length=20), nullable=False, unique=True)
    posts = db.relationship('Post', backref='user', lazy=True, cascade='delete')


    def __init__(self, username, password):
        self.name = username
        self.password = password

    def __repr__(self) -> str:
        return f'User {self.name}'

    #Register user function
    def save(user_data):
        db.session.add(user_data)
        db.session.commit()

    #Delete user information
    def delUser(user_data):
        db.session.delete(user_data)
        db.session.commit()

#投稿用のクラス
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    content = db.Column(db.String(length=20), nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))


    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def __repr__(self) -> str:
        return f'Post {self.content}'

    #投稿
    def post(post_data):
        db.session.add(post_data)
        db.session.commit()

    #投稿削除
    def delPost(post_data):
        db.session.delete(post_data)
        db.session.commit()

db.create_all()