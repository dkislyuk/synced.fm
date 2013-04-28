from server import db
from flask import Blueprint, request, json

from classifier.models import DataSet
from classifier.conn import classifier_location, conn_str

from mongokit import Connection
from mongokit import ObjectId

import requests

training_api = Blueprint('training_api', __name__)


@training_api.route('/api/training_set', methods=['POST'])
def create_training_set():
    training_set = db.get_connection([DataSet]).DataSet()
    data = json.loads(request.data)
    
    training_set.s3_links   = data['s3_links']
    training_set.name       = data['name']
    training_set.config     = data['config']
     
    training_set.save();
    
    payload = {'dataset_id': str(training_set._id)}

    requests.post(classifier_location + '/train', payload)
    
    return str(training_set._id)

@training_api.route('/api/training_set', methods=['GET'])
@training_api.route('/api/training_set/<train_set_id>', methods=['GET'])
def get_training_set(train_set_id=None):
    training_set = db.find(DataSet, train_set_id)
    
    return training_set
    
    #training_set = db.get_connection([DataSet]).DataSet.find_one()
    
    #training_set = self.connection.DataSet.one({"_id": ObjectId(train_set_id)})
    
    #training_set = db.get_connection([DataSet]).DataSet.one({"_id": ObjectId(train_set_id)})
    #training_set = db.find(DataSet, train_set_id)
    
    
    #return training_set
    # connection = db.get_connection([Track])

    # if track_id == None:
    #     result = [track for track in connection.Track.find()]
    #     return result
    # else:
    #     return "Not implemented yet."
