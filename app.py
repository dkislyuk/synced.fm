import os, sys
from api import API
from flask import Flask, jsonify, render_template, url_for, request, json
from mongokit import Connection

class MyFlask(Flask):
    def make_response(self, rv):
        if hasattr(rv, 'to_json'):
            return jsonify(rv.to_json())
        return Flask.make_response(self, rv)

app = Flask(__name__)
api = API()

@app.route('/api/track/create', methods=['POST'])
def create_track():

    return api.create_track(request.data)

@app.route('/api/track/<action>', methods=['POST'])
def track(action):
    ret = api.get_track(123)
    
    #app.logger.debug(' event: ', ret)
    return ret.to_json()

@app.route('/api/user/login', methods=['POST'])
def login():
    status = api.login(request.data)
    
    return status.to_json()

@app.route('/api/user/signup', methods=['POST'])
def signup():
    status = api.create_user(request.data)
    
    return status


@app.route('/')
@app.route('/<section>')
@app.route('/<section>/<action>')
def index(section = None, action = None):
    return render_template('index.html')

if __name__ == '__main__':
    print "running";
    # Bind to PORT if defined, otherwise default to 5000.
    #port = int(os.environ.get('PORT', 5000))
    port = 2727
    app.run(host='0.0.0.0', port=port, debug=True)
