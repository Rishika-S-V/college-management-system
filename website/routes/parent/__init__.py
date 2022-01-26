from flask import Blueprint
from flask_login import current_user

parent = Blueprint("parent", __name__)

@parent.before_request
def before_request():
    # print(f"[CALLBACK] {request.path} ...")
    if "Parent" != current_user.role.role_name:
        return "<h1>Unauthorized Access</h1>"

from . import view
from . import utils