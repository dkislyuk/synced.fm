from server import db

from flask import Blueprint, request
from server.models.track import Track

training_api = Blueprint('training_api', __name__)


@track_api.route('/api/training_set', methods=['POST'])
def create_track():
    connection = db.get_connection([Track])
    track = connection.Track.from_json(request.data)

    #track.initialize()
    track.save()

    return track



@track_api.route('/api/training_set', methods=['GET'])
@track_api.route('/api/training_set/<int:train_set_id>', methods=['GET'])
def get_track(track_id=None):
    pass
    # connection = db.get_connection([Track])

    # if track_id == None:
    #     result = [track for track in connection.Track.find()]
    #     return result
    # else:
    #     return "Not implemented yet."
