from __init__ import db, cursor, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # columns
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        """init"""
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check Password"""
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


class Post(db.Model):
    __tablename__ = 'blog_data_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    content = db.Column(db.String(5000))

    def __init__(self, title, content):
        self.title = title
        self.content = content


class Ecpay_data(db.Model):
    __tablename__ = 'Ecpay_db'
    id = db.Column(db.Integer, primary_key=True)
    