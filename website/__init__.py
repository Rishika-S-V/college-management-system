from os import environ as env
import json
from flask import Flask, render_template, request
from flask_fontawesome import FontAwesome

app = Flask(__name__)

@app.route('/admin-login')
def admin_login():
    return render_template("login/admin_login.html.j2")


@app.route('/general-login')
def general_login():
    return render_template("login/general_login.html.j2")