from flask import Flask
#from flask_mail import Mail
from .extensions import db, moment, mail, bootstrap, migrate, cors, bcrypt, ma, login_manager
from config import config

#mail = Mail()
def __call__(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')

    return app