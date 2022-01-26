from . import parent
from flask_login import login_required, current_user


@parent.route("/")
@login_required
def home():
    return f"<h1>Parent Homepage</h1>{current_user.u_name}<p></p>"
