import imp
from flask import Flask

from .commands import create_tables, create_admin
from .extensions import db, login_manager
from . import models
from . import constants
from . import routes 

def create_app(config_file = "settings.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Commands
    app.cli.add_command(create_tables)
    app.cli.add_command(create_admin)
    
    # Blueprints
    app.register_blueprint(routes.common, url_prefix="/common")
    app.register_blueprint(routes.parent, url_prefix="/parent")
    app.register_blueprint(routes.student, url_prefix="/student")
    app.register_blueprint(routes.staff, url_prefix="/staff")
    
    constants.query_constants(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(user_id)    
    
    return app

