from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    s = Server(app.wsgi_app)
    s.serve(host="0.0.0.0", port=5500)
