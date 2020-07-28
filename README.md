# Full Stack Udacity Project 2: Trivia

The backend for a casting agency website. The capstone project for the Full Stack Udacity nanodegree.

## Usage
CD into the backend folder. Create a virtual environment and install the required backend dependencies by running ```$ pip install -r requirements.txt```. A database called 'casating' should exist on a server using the default listening port (5432). You must set environment variables for DB_USER and DB_PASS. Then run these commands to run the server:

```
$ export FLASK_APP=flaskr
$ flask run
```

The server will now be running at localhost:5000.

## Tests
Unit tests can be run by running the command ```pytest``` inside of the backend directory.
