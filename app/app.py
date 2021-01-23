import os
import settings
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from controllers.registry import search_licensee

application = Flask(__name__)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(application)
db = mongo.db

def hide_email(email):
    m = email.split('@')
    return f'{m[0][0]}{"*"*(len(m[0])-2)}{m[0][-1] if len(m[0]) > 1 else ""}@{m[1]}'

@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the ULI Registry app!'
    )

@application.route('/query', methods=['POST'])
def licensee():
    item = {}
    data = []
    post_data = request.get_json(force=True)
    possible_matches = 0

    if post_data["email"] is not None:
        _licensees = db.registry.find({ 'email':post_data["email"] })

    for licensee in _licensees:
        possible_matches += 1
        item = {
             'id': str(licensee['_id']),
             'email': hide_email(licensee['email']),
             'firstname': licensee['firstname'],
             'lastname': licensee['lastname'],
             'nrds': licensee['nrds']
         }
        data.append(item)

    if possible_matches == 0:
        _licensees = db.registry.find({"$and": [{"firstname": post_data["firstname"]}, 
                                                {"lastname": post_data["lastname"]}]})
        for licensee in _licensees:
            possible_matches += 1
            item = {
            'uid': str(licensee['_id']),
            'email': hide_email(licensee['email']),
            'firstname': licensee['firstname'],
            'lastname': licensee['lastname'],
            'licenseNumber': licensee['licenseNumber'],
            'nrds': licensee['nrds']
            }
            data.append(item)

    
    data.append({"Possible Matches:" : possible_matches})
    return jsonify(
        status=True,
        data=data
    )

@application.route('/register', methods=['POST'])
def createLicensee():
    data = request.get_json(force=True)
    item = {
        'nrds': data["nrds"],
        'firstname': data["firstname"],
        'lastname': data["lastname"],
        'email': data["email"],
        'licenseNumber': data["licenseNumber"]
    }
    db.registry.insert_one(item)

    return jsonify(
        status=True,
        message='ULI saved successfully!'
    ), 201

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)