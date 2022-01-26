from flask import render_template

from . import common

@common.route("/login")
def login():
    return render_template("login/general_login.html.j2")