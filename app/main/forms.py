from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, IntegerField, PasswordField, RadioField,
    FileField
)
from wtforms.validators import DataRequired
'''
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')
'''
class LoginForm(FlaskForm):
    username = StringField('Name or Username', validators=[DataRequired()])