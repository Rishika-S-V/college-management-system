from contextlib import redirect_stderr
from typing import Dict, List, Union
from flask import make_response, redirect, request, jsonify, url_for
from flask_login import login_user
from datetime import datetime, timedelta
import json

from . import common
from ... import models
from ... import constants


@common.route("/login-val", methods=["POST"])
def login_val():
    redirect_url = None
    
    req: Dict[Union[str, list]] = json.loads(request.data)
    print(req)

    # Getting data from js
    u_name: str = req.get("general-login-form__username-input-field")
    pass_: str = req.get("general-login-form__password-input-field")
    remember_me: List = req.get("general-login-form__remember-me-check-box")
    role: models.Role = req.get("roles-input")
    if role == "student":
        role = constants.ROLE.STUDENT
        redirect_url = url_for("student.home")
    elif role == "staff":
        role = constants.ROLE.STAFF
        redirect_url = url_for("staff.home")
    else:
        role = constants.ROLE.PARENT
        redirect_url = url_for("parent.home")

    user: models.User = (
        models.User.query.filter(
            (models.User.u_name == u_name) | (models.User.email == u_name)
        )
        .filter(models.User.role == role)
        .first()
    )
    
    
    remember_me:bool = True if remember_me else False
    status = True if user and user.password == pass_ else False
    errors = {k:"" for k in req.keys()}

    print(errors)
    
    if status:
        login_user(user, remember=remember_me)
    
    else:
        if not user:
            errors['general-login-form__username-input-field'] = "Invalid Username or Email."
        elif not status and user:
            errors['general-login-form__password-input-field'] = "Invalid Password."
            
    res = {"status": status,
           "redirect_url": redirect_url if status else "",
           "errors": errors
           }

    res = make_response(jsonify(res))
    res.set_cookie("role", value=role.role_name.lower(), expires=datetime.now()+timedelta(weeks=30))

    return res
