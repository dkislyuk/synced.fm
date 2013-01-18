import sys
from server import db

from flask import Blueprint, request, current_app
from server.models.track import Track

track_api = Blueprint('track_api', __name__)


@track_api.route('/api/track', methods=['POST'])
def create_track():
    connection = db.get_connection([Track])
    track = connection.Track.from_json(request.data)

    track.save()

    return track


@track_api.route('/api/track', methods=['POST'])
def update_track():
    return "Not implemented yet."


@track_api.route('/api/track/0', methods=['GET'])
def get_empty_track():
    #connection = db.get_connection([Track])
    return Track()


@track_api.route('/api/track', methods=['GET'])
@track_api.route('/api/track/<int:track_id>', methods=['GET'])
def get_track(track_id=None):

    connection = db.get_connection([Track])

    if track_id == None:
        result = [track for track in connection.Track.find()]
        return result
    else:
        return "Not implemented yet."
