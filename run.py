import os
from app.extensions import migrate
from app import __call__, db

app = __call__(os.getenv('HOS_CONFIG') or 'default')
migrate.init_app(app, db)