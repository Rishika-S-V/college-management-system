from flask import Flask, render_template
from website import app
from livereload import Server

 
if __name__ == "__main__":
    s = Server(app.wsgi_app)
    s.serve(host="0.0.0.0", port=5500)
