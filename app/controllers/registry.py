import json
from controllers.mongo import db, request

def search_licensee(post_data):
    item = {}
    data = []
   
    possible_matches = 0

    if post_data["email"] is not None:
        _licensees = db.registry.find({ 'email': post_data["email"] })

    for licensee in _licensees:
        possible_matches += 1
        item = {
             'id': str(licensee['_id']),
             'email': hide_email(licensee['email']),
             'firstname': licensee['firstname'],
             'lastname': licensee['lastname'],
             'licenseNumber': licensee['licenseNumber'],
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

    
    data.append({"possible_matches:" : possible_matches})
    if possible_matches == 0:
        return None
    else:
        return data

def hide_email(email):
    m = email.split('@')
    return f'{m[0][0]}{"*"*(len(m[0])-2)}{m[0][-1] if len(m[0]) > 1 else ""}@{m[1]}'

def create_licensee(post_data):
    item = {
        'nrds': post_data["nrds"],
        'firstname': post_data["firstname"],
        'lastname': post_data["lastname"],
        'email': post_data["email"],
        'licenseNumber': post_data["licenseNumber"]
    }
    uli = db.registry.insert_one(item).inserted_id
    print(uli)
    return uli
