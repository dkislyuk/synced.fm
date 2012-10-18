from flask import Blueprint, request, current_app, jsonify
from server.models.user import User

from flask.ext.login import *

from server import login_manager, db
import json

user_api = Blueprint('user_api', __name__)

@user_api.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    
    login_user(user_id)
    
    pass

@user_api.route('/api/user', methods=['POST'])    
def create_user():
    connection = db.get_connection([User])
    user = connection.User.from_json(request.data)

    user.save()

    return user

@user_api.route('/api/user/login', methods=['POST'])
def login_user_func():
    return "dkislyuk"
    
#    username = json.loads(request.data)['username']
#    connection = db.get_connection([User])
#    
#    u = connection.User.find_one({"username" : username})
#    #User = connection.find_one(username)
#    
#    login_user(u)
#    
#    return u

@login_manager.user_loader
def load_user(username):
    connection = db.get_connection([User])
    u = connection.User.find_one(username)
    
    return User

