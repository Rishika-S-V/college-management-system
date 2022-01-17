from os import environ as env
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("login/admin_login.html.j2")
