from flask import Blueprint, request, current_app
from models.user import User
#from app import login_manager
#from api import app

user_api = Blueprint('user_api', __name__)

@user_api.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    pass

@user_api.route('/api/user/create', methods=['POST'])    
def create_user(params):
    pass

@user_api.route('/api/login', methods=['POST'])
def login(params):
    pass


#@current_app.login_manager.user_loader
def load_user(userid):
    return current_app.login_manager

