# Centralized ULI Registry Proof of Concept
Welcome to the rough proof of concept of a centralized ULI Service


## Tech Stack
* Python 3 Flask API 
* Mongo DB
* NGINX Reverse Proxy w/ Gunicorn
* Docker Compose


To run, simply bring up the webserver, web app,  and database with the following command.

    docker-compose build
    docker-compose up -d

# Registering a User
To register a user

    POST http://localhost/register 
    {
        "nrds": "08400162342349", 
        "licenseNumber": "12354",
        "email": "dconroy1234@gmail.com",
        "firstname" : "David",
        "lastname" : "Conroy"
    }

## Sample Return - No Match Found, New User Created
    {
        "ULI": "600c5b0d762ace88ef66f2ca",
        "message": "ULI saved successfully!",
        "status": true
    }
## Sample Return - Potential Matches Found

    {
        "data": [
            {
                "email": "d*********4@gmail.com",
                "firstname": "Dave",
                "id": "600b47f1904fc2120998cf9c",
                "lastname": "Conroy",
                "licenseNumber": "1234",
                "nrds": "084001679"
            },
            {
                "email": "d*********4@gmail.com",
                "firstname": "Dave",
                "id": "600b72d51a9c4dd089e27978",
                "lastname": "Conroy",
                "licenseNumber": "12354",
                "nrds": "08400162342349"
            },
            {
                "possible_matches:": 2
            }
        ],
        "message": "ULI May Exist!",
        "status": true
    }

# Querying a User
Sample POST to http://localhost/query

    {
        "nrds": "08400162342349", 
        "licenseNumber": "12354",
        "email": "dconroy1234@gmail.com",
        "firstname" : "David",
        "lastname" : "Conroy"
    }
## Sample Return - Single Match Found
    {
        "data": [
            {
                "email": "d*****y@gmail.com",
                "firstname": "Dave",
                "lastname": "Conroy",
                "licenseNumber": "1234",
                "nrds": "084001679",
                "uid": "600b47ad904fc2120998cf9b"
            },
            {
                "possible_matches:": 1
            }
        ],
        "message": "ULI May Exist!",
        "status": true
    }

## Sample Return - Multiple Matches Found
    {
        "data": [
            {
                "email": "d*****y@gmail.com",
                "firstname": "Dave",
                "lastname": "Conroy",
                "licenseNumber": "1234",
                "nrds": "084001679",
                "uid": "600b47ad904fc2120998cf9b"
            },
            {
                "email": "d*********4@gmail.com",
                "firstname": "Dave",
                "lastname": "Conroy",
                "licenseNumber": "12354",
                "nrds": "08400162342349",
                "uid": "600b72d51a9c4dd089e27978"
            },
            {
                "possible_matches:": 2
            }
        ],
        "message": "ULI May Exist!",
        "status": true
    }


## Outstanding Questions

1) Is mongo the right technology for this? Will it scale to millions of users?
2) Can the matching be improved? Right now only doing email, or combination of first and last name. How can we ensure millisecond response time on multiple search types on a NOSQL collection? Elastic Search?
3) Do I need to nest the license information like the DID spec?
4) How do we avoid leaking data?
   1) Do we need to obsfucate license numbers? 
   2) NRDS?
   3) Names?
5) Do we need to deploy this?