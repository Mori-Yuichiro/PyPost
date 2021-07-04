from enum import unique
from sqlalchemy.orm import backref
from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    password = db.Column(db.String(length=20), nullable=False, unique=True)
    # posts = db.relationship('Post', backref='user', lazy=True)

    db.create_all()

    def __init__(self, username, password):
        self.name = username
        self.password = password

    def __repr__(self) -> str:
        return f'User {self.name}'

    def save(user_data):
        db.create_all()
        db.session.add(user_data)
        db.session.commit()
