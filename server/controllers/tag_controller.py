from flask import Blueprint, request, current_app
from models.tag import Tag

tag_api = Blueprint('tag_api', __name__)

@tag_api.route('/api/tag/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    pass

@tag_api.route('/api/tag/create', methods=['POST'])    
def create_tag(params):
    pass
