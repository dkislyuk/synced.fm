import os

from flask import _app_ctx_stack
from flask import Flask, jsonify, render_template, url_for, request, json
from flask.ext.mongoengine import MongoEngine

import db

from controllers.track_controller import track_api
from controllers.tag_controller import tag_api
from controllers.user_controller import user_api
 
# Global JSON return
class MyFlask(Flask):
    def make_response(self, rv):
        if hasattr(rv, 'to_json'):
            return jsonify(rv.to_json())
        return Flask.make_response(self, rv)

app = MyFlask(__name__)
app.config.from_pyfile('config/app.conf')
db_engine = MongoEngine(app)
db_engine.init_app(app)

db.init_app(app)


app.register_blueprint(track_api)
app.register_blueprint(tag_api)
app.register_blueprint(user_api)

@app.route('/api/user/login', methods=['POST'])
def login():
    status = api.login(request.data)
    return status.to_json()

@app.route('/api/user/signup', methods=['POST'])
def signup():
    status = api.create_user(request.data)
    return status.to_json()


@app.route('/')
@app.route('/<section>')
@app.route('/<section>/<action>')
def index(section = None, action = None):
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
