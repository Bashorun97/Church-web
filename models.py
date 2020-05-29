import hashlib
from app import db, login_manager, ma
from flask import current_app
import datetime as d
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100), index=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    age = db.Column(db.Integer)
    hashed_password = db.Column(db.String(128))
    telephone = db.Column(db.String(50), unique=True)
    house_address = db.Column(db.String(120))
    worker = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    profile_picture_url = db.Column(db.String(50))
    users = db.relationship('Article', backref='poster')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)    
        if self.is_admin is None:
            if self.email == current_app.config['RCCG_HOS_ADMIN']:
                self.is_admin = True
            if self.is_admin is None:
                self.admin = False
    
    @property
    def password(self):
        raise AttributeError(f'Password field isn\'t readable')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)
    

class Article(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    story = db.Column(db.Text)
    story_title = db.Column(db.Text, nullable=False)
    time_posted = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def date_posted(self):
        self.time_posted = d.datetime.utcnow()

@login_manager.user_loader
def load_user(user_id):
    l = User.query.get(int(user_id))
    print(l.name)
    return User.query.get(int(user_id))

class UserSchema(ma.Schema):
    class Meta: 
        model = User
        fields = (
            'id', 'name', 'surname', 'usernmae', 'email', 'age', 'telephone',
            'house_address', 'profile_picture'
        )
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class ArticleSchema(ma.Schema):
    class Meta:
        model = Article
        fields = (
            'id', 'story', 'story_title', 'time_posted'
        )
article_schema = Article()
