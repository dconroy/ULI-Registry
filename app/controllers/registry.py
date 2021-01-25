import json
from controllers.mongo import db, request
from controllers.utils import hide_email

def search_licensee(post_data):
    item = {}
    data = []
    possible_matches = 0

    if post_data['nrds'] is not None:
        _licensees = db.registry.find({ 'nrds': post_data['nrds'] })
        for licensee in _licensees:
            if(post_data['firstname'] == licensee['firstname'] and post_data['lastname'] == licensee['lastname']):
                possible_matches += 1
                item = {
                'uli': str(licensee['_id']),
                'email': hide_email(licensee['email']),
                'firstname': licensee['firstname'],
                'lastname': licensee['lastname'],
                'license_data': licensee['license_data'],
                'nrds': licensee['nrds']
                }
                data.append(item)

    data.append({'possible_matches:' : possible_matches})

    if possible_matches == 0:
        return None
    else:
        return data

def create_licensee(post_data):
    item = {
        'nrds': post_data['nrds'],
        'firstname': post_data['firstname'],
        'lastname': post_data['lastname'],
        'email': post_data['email'],
        'license_data': post_data['license_data']
    }
    uli = db.registry.insert_one(item).inserted_id
    return uli
