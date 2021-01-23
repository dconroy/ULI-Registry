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

You will need to create a database user for the flask app to save data to Mongo

    $ docker exec -it mongodb bash

Once inside the container, login to mongo

    root@c5a67fc9927b:/# mongo -u mongodbuser -p

You will be prompted for the password that you entered as the value for the MONGO_INITDB_ROOT_PASSWORD variable in the docker-compose.yml file. The password can be changed by setting a new value for the MONGO_INITDB_ROOT_PASSWORD in the mongodb service, in which case you will have to re-run the docker-compose up -d command.

Run the show dbs; command to list all databases:

    mongodb> show dbs;

You should see:

    Output
    admin    0.000GB
    config   0.000GB
    local    0.000GB
    5 rows in set (0.00 sec)


The admin database is a special database that grants administrative permissions to users. If a user has read access to the admin database, they will have read and write permissions to all other databases. Since the output lists the admin database, the user has access to this database and can therefore read and write to all other databases.

Saving the first licensee will automatically create the MongoDB database. MongoDB also allows you to switch to a database that does not exist using the use database command. It creates a database when a document is saved to a collection. Therefore the database is not created here; that will happen when you save your first licensee in the database from the API. Execute the use command to switch to the flaskdb database:

    mongdob> use flaskdb

Next, create a new user that will be allowed to access this database:

    mongdob> db.createUser({user: 'flaskuser', pwd: 'your_mongodb_password', roles: [{role: 'readWrite', db: 'flaskdb'}]})
    mongodb> exit

This command creates a user named flaskuser with readWrite access to the flaskdb database. Be sure to use a secure password in the pwd field. The user and pwd here are the values you defined in the docker-compose.yml file under the environment variables section for the flask service.



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

1) Is mongo the right technology for this?
2) Can the matching be improved? Right now only doing email, or combination of first and last name
3) How do we avoid leaking data?
   1) Do we need to obsfucate license numbers? 
   2) NRDS?
   3) Names?