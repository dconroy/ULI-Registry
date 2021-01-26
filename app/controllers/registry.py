import json
from controllers.mongo import db, request
from controllers.utils import hide_email, ordered, format_item

def search_licensee(post_data):
    data = []
    possible_matches = 0
    #check NRDS, and if matches, confirm first name last name match
    if post_data["nrds"] is not None:
        _licensees = db.registry.find({ "nrds": post_data["nrds"] })
        for licensee in _licensees:
            if(post_data["firstname"] == licensee["firstname"] and post_data["lastname"] == licensee["lastname"]):
                possible_matches += 1
                data.append(format_item(licensee))

    #If no NRDS search first name, last name, then check licenses
    if possible_matches == 0:
        _licensees = db.registry.find({"$and": [{"firstname": post_data["firstname"]}, 
                                                {"lastname": post_data["lastname"]}]})
        
        for licensee in _licensees: #for each licensee with the same first/last name
            for check_license in post_data["license_data"]: # and every license type provided in the search
                for license_held in licensee["license_data"]:
                    if(ordered(check_license) == ordered(license_held)):
                        possible_matches += 1
                        data.append(format_item(licensee))
                        break
                    
    data.append({"possible_matches:" : possible_matches})

    if possible_matches == 0:
        return None
    else:
        return data

def create_licensee(post_data):
    item = {
        "nrds": post_data["nrds"],
        "firstname": post_data["firstname"],
        "lastname": post_data["lastname"],
        "email": post_data["email"],
        "license_data": post_data["license_data"]
    }
    uli = db.registry.insert_one(item).inserted_id
    return uli
