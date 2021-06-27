from sqlalchemy.orm import backref
from app import db

# db.create_all()


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=20), nullable=False)
    password = db.Column(db.String(length=20), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

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


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    content = db.Column(db.String(length=200), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    # def __init__(self, content, user_id):
    #     self.content = content
    #     self.user_id = user_id

    def __repr__(self) -> str:
        return f'Post {self.content}'

    def post(content):
        db.create_all()
        db.session.add(content)
        db.session.commit()
