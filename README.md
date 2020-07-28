# Full Stack Udacity Capstone: Casting

The backend for a casting agency website. The capstone project for the Full Stack Udacity nanodegree.

## Usage (deployed API)
The API can be accessed at https://capstone-fs-udacity.herokuapp.com/. See the API reference for a full list of endpoints.

All requests require a JWT in the authorization header. The setup.sh script will set these JWTs at ```EXECUTIVE_PRODUCER_TOKEN```, ```CASTING_DIRECTOR_TOKEN```, and ```CASTING_ASSISTANT_TOKEN```. These tokens will only be valid for a certain period of time. If you need to regenerate tokens, visit the auth0 login page (provided in authURL.txt or you can create it using the variables provided in setup.sh) and login using one of these users. 

Executive producer: executive_producer@gmail.com, Password1
Casting director: casting_director@gmail.com, Password1
Casting assistant: casting_assistant@gmail.com, Password1

For more information on the roles, see RBAC.

## Usage (local development server)
Create a virtual environment and install the required backend dependencies by running ```$ pip install -r requirements.txt```.

You should have a database named 'casting' listening at the default port (5432).

To start the server, run the following commands:
```
$ source setup.sh
$ flask run
```

The server will now be running at localhost:5000. You may need to update the DATABASE_URL variable with the database username and password if required.

## Endpoints

### GET /actors
Fetches the list of all actors.
Arguments: none
Returns: an object with an actors field. Each actor is an object containing id, name, age, and gender.
```
{
    "actors": [
        {
            "age": 89,
            "gender": "male",
            "name": "Actor name",
            "id": 1
        }
    ],
    "success": true
}
```

### GET /movies
Fetches the list of all movies.
Arguments: none
Returns: an object with a movies field. Each movie is an object containing id, title, and release date (```release```).
```
{
    "movies": [
        {
            "id": 1,
            "release": "Mon, 27 Jul 2020 16:29:30 GMT",
            "title": "Bad Movie"
        }
    ]
}
```

### POST /actors
Creates a new actor.
Arguments: In the body of the request, an object specifying the actor's name, age, and gender.
Returns: an object that contains only the success field.
```
{
    "success": true
}
```

### POST /movies
Creates a new movie.
Arguments: In the body of the request, an object specifying the movie's title and release date (```release```).
Returns: an object that contains only the success field.
```
{
    "success": true
}
```

### DELETE /actors/{actor_id}
Deletes an actor.
Arguments: none
Returns: an object that contains only the success field.
```
{
    "success": true
}
```

### DELETE /movies/{movie_id}
Deletes a movie.
Arguments: none
Returns: an object that contains only the success field.
```
{
    "success": true
}
```

### PATCH /actors/{actor_id}
Updates an actor with new data.
Arguments: In the body of the request, an object specifying the actor's name, age, and gender.
Returns: an object that contains only the success field.
```
{
    "success": true
}
```

### PATCH /movies/{movie_id}
Updates a movie with new data.
Arguments: In the body of the request, an object specifying the movie's title and release data (```release```).
Returns: an object that contains only the success field.
```
{
    "success": true
}
```

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": false,
    "error": 400,
    "message": "Bad request."
}
```

## RBAC

### Executive Producer
GET /actors
GET /movies
POST /actors
POST /movies
DELETE /actors
DELETE /movies
PATCH /actors
PATCH /movies

### Casting Director
GET /actors
GET /movies
POST /actors
DELETE /actors
PATCH /actors
PATCH /movies

### Casting Assistant
GET /actors
GET /movies


## Tests
Unit tests can be run by running the command ```pytest```. These tests will automatically use the JWTs provided in the .env files.
