import json
from controllers.mongo import db, request
from controllers.utils import hide_email, ordered, format_uli

def match_licenses(licensees, licenses_to_check):
    for licensee in licensees: #for each licensee 
        for individual_license in licenses_to_check: # and every license provided in the search
            for license_held in licensee["license_data"]:
                if(ordered(individual_license) == ordered(license_held)): #order the json to make sure you get exact matches
                    return licensee

def search_licensee(post_data):
    data = []
    possible_matches = 0

    #check NRDS, and if matches, confirm first name last name match
    if post_data["nrds"] is not None:
        _licensees = db.registry.find({ "nrds": post_data["nrds"] })
        for licensee in _licensees:
            if(post_data["firstname"] == licensee["firstname"] and post_data["lastname"] == licensee["lastname"]):
                possible_matches += 1
                data.append(format_uli(licensee))

    #If no NRDS search first name, last name, then check licenses
    if possible_matches == 0:
        #temp store licensees that are matched by license data
        matched_by_license = [] 

        #get the licenses provided by the search for comparison against licenses held by people with same first and last name
        licenses_to_check = post_data["license_data"] 

        #pull users with matching first/last
        _licensees = db.registry.find({"$and": [{"firstname": post_data["firstname"]}, 
                                                {"lastname": post_data["lastname"]}]})
        
        #check every license submitted against every license held by people with same first and last name
        matched_by_license = match_licenses(_licensees, licenses_to_check)
        if matched_by_license is not None:
            possible_matches += 1
            data.append(format_uli(matched_by_license))
                
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
