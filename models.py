import hashlib
import datetime as d
import jwt, json
from app import db, login_manager, ma
from flask import current_app
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
    confirmed = db.Column(db.Boolean, default=False)
    users = db.relationship('Article', backref='poster')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)    
        if self.is_admin is None:
            if self.email == current_app.config['RCCG_HOS_ADMIN']:
                self.is_admin = True
            if self.is_admin is None:
                self.admin = False

    """========= Password Verification Starts ========="""

    @property
    def password(self):
        raise AttributeError(f'Password field isn\'t readable')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)
    

    """========= Account Authentication Starts ========="""
    # jwt for account confirmation
    def generate_json_web_confirmation_token(self):
        token = jwt.encode({'user_id':self.id, 'exp':d.datetime.utcnow() + d.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
        return token #dumps
    
    def confirm_token(self, token):
        try:
            key = jwt.decode(token, current_app.config['SECRET_KEY']) #loads
        except:
            return False
        # get user_id for dictionary "key"
        if key.get('user_id') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
        

    """========= Change of Password Confirmation starts ========="""

    def generate_json_web_token_for_password_reset(self):
        token = jwt.encode({'reset':self.id, 'exp':d.datetime.utcnow() + d.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
        return token
    
    @staticmethod
    def reset_password(self, token, new_password):
        try:
            key = jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return False

        '''
        Difference between reset_password and confirm_token is that the former method
        tries to determine a user by extracting the user object directly from the database
        unlike confirm_token that merely uses user_id as a component for crytographically
        creating and deciphering a token
        '''

        user = User.query.get(key.get('reset'))
        if user is None:
            return False
        user.passoword = new_password
        db.session.add(user)
        return True
    
    """========= Ends - Change of Password Confirmation ========="""


    """========= Change of Email Confirmation starts ========="""
    def generate_json_web_token_for_email_change(self, new_mail):
        token = jwt.encode({'change-email':self.id, 'exp':d.datetime.utcnow() + d.timedelta(minutes=30), 'new_mail':new_mail}, current_app.config['SECRET_KEY'])
        return token
    
    def change_email(self, token):
        try:
            key = jwt.decode(token, current_app.config['SECRET_KEY'])
        except InvalidSignatureError:
            return False
        except:
            return False
        if key.get('change-email') != self.id:
            return False
        if key.get('new_mail') is None:
            return False
        if User.query.filter_by(email=new_mail).first() is not None:
            return False
        self.email = new_mail
        db.session.add(self)
        return True
        
        
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
