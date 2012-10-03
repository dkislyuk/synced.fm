from server import app
from flask import render_template, url_for, request

@app.route('/')
@app.route('/<section>')
@app.route('/<section>/<action>')
def index(section = None, action = None):
    return render_template('index.html')