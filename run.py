import os
from app.extensions import migrate
from app import __call__, db
from models import User, Article

app = __call__(os.getenv('HOS_CONFIG') or 'default')
migrate.init_app(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Article=Article)