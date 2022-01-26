from flask import Blueprint
from flask_login import current_user

from ... import constants

student = Blueprint("student", __name__)

@student.before_request
def before_request():
    # print(f"[CALLBACK] {request.path} ...")
    if constants.ROLE.STUDENT != current_user.role.role_name:
        return "<h1>Unauthorized Access</h1>"

from . import view
from . import utils