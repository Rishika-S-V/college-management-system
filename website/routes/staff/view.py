from . import staff
from flask_login import login_required, current_user


@staff.route("/")
@login_required
def home():
    return f"<h1>Staff Homepage</h1>{current_user.u_name}<p></p>"
