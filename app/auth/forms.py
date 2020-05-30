from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, IntegerField, PasswordField, BooleanField
)
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError
from models import User

class RegistrationForm(FlaskForm):
    name = StringField('Name')
    surname = StringField('Surname')
    username = StringField('Username', validators=[
        DataRequired(), Length(4, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    #age = IntegerField('Age', validators)
    password  = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    telephone = StringField('Telephone number', validators=[Length(11)])
    house_address = StringField('Home address', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
    
    def validate_telephone(self, field):
        if User.query.filter_by(telephone=field.data).first():
            raise ValidationError('Telephone already in use')


class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')  


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired(), EqualTo('password2',
    message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Submit', validators=[DataRequired()])
