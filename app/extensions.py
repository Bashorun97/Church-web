from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_moment import Moment 
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()
migrate = Migrate()
cors = CORS()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'auth.view'


import re
#from models import User

def emailcheck(str):
    """
        emailCheck uses regex via python3's re module to verify
        that received argument is indeed an email address.
        -------
        type(argument) == <str_class>
        type(return) == <bool_class>

        emailcheck can also find an email address from within any
        string text, returns False if it finds none.
    """

    emailreg = re.compile(r'''
        # username
        ([a-zA-Z0-9_\-+%]+|[a-zA-Z0-9\-_%+]+(.\.))
        # @ symbol
        [@]
        # domain name
        [a-zA-Z0-9.-]+
        # dot_something
        (\.[a-zA-Z]{2,4})
    ''',re.VERBOSE)
    try:
        if emailreg.search(str):
            return True
        else:
            return False
    except AttributeError:
        raise False
'''
def telephone_check(form):
    data = form.telephone.data
    tel = User.query.filter_by(telephone=data).first()
    if tel:
        return True
    else:
        return False
'''