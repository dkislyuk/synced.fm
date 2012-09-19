from flask import Blueprint, request, current_app
from models.user import User

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

