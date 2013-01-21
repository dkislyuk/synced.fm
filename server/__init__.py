#from flask import _app_ctx_stack
from flask import Flask, jsonify
#from flask.ext.mongoengine import MongoEngine
from flask.ext.login import *

from server import db

# Global JSON return
class MyFlask(Flask):
    def make_response(self, rv):
        if hasattr(rv, 'to_json'):
            return jsonify(rv.get_json())
        return Flask.make_response(self, rv)

app = MyFlask(__name__)
app.config.from_object('config')
#db_engine = MongoEngine(app)
#db_engine.init_app(app)

db.init_app(app)
login_manager = LoginManager()
login_manager.setup_app(app)

from server.controllers.track_controller import track_api
from server.controllers.tag_controller import tag_api
from server.controllers.user_controller import user_api

app.register_blueprint(track_api)
app.register_blueprint(tag_api)
app.register_blueprint(user_api)

import server.views
