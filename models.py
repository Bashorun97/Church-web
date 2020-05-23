from app import db, login_manager
from flask import current_app

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    age = db.Column(db.Integer)
    password_hash = db.Column(db.String)
    telephone = db.Column(db.String(50), unique=True)
    house_address = db.Column(db.String(120))
    worker = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    profile_picture_url = db.Column(db.String(50))
    users = db.relationship('Article', backref='poster')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.is_admin is False:
            print(self.is_admin)
            if self.email == current_app.config['RCCG_HOS_ADMIN']:
                self.is_admin = True


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    story = db.Column(db.Text)
    story_title = db.Column(db.Text, nullable=False)
    time_posted = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)