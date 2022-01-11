from flask import Flask

from .commands import create_tables
from .extensions import db, login_manager
from . import models

def create_app(config_file = "settings.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    
    db.init_app(app)
    
    app.cli.add_command(create_tables)
    
    # db.create_all()
    
    
    return app

def create_db(app: Flask):
    pass
