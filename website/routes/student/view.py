from . import student
from flask_login import login_required, current_user


@student.route("/")
@login_required
def home():
    return f"<h1>Student Homepage</h1>{current_user.u_name}<p></p>"
