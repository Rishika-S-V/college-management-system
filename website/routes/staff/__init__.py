from flask import Blueprint
from flask_login import current_user

staff = Blueprint("staff", __name__)

@staff.before_request
def before_request():
    # print(f"[CALLBACK] {request.path} ...")
    if "Staff" != current_user.role.role_name:
        return "<h1>Unauthorized Access</h1>"

from . import view
from . import utils