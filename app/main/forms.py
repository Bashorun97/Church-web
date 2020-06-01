from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, IntegerField
)
from wtforms.validators import DataRequired, Length, Regexp
from wtforms import ValidationError
from models import User

class EditProfileForm(FlaskForm):
    name = StringField('Name')
    surname = StringField('Surname')
    username = StringField('Username', validators=[
        DataRequired(), Length(4, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    #age = IntegerField('Age', validators)
    house_address = StringField('Home address', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered. Please choose a different one')