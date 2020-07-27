from .flaskr import create_app
from .models import db, Actor, Movie
import os
import json
import pytest
from dotenv import load_dotenv
from datetime import datetime


DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# Load JWT tokens from .env file and create respective headers.
load_dotenv()
EXECUTIVE_PRODUCER_TOKEN = os.getenv('EXECUTIVE_PRODUCER_TOKEN')
EXECUTIVE_PRODUCER_HEADER = {'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)}

CASTING_DIRECTOR_TOKEN = os.getenv('CASTING_DIRECTOR_TOKEN')
CASTING_DIRECTOR_HEADER = {'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)}

CASTING_ASSISTANT_TOKEN = os.getenv('CASTING_ASSISTANT_TOKEN')
CASTING_ASSISTANT_HEADER = {'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)}


@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    database_path = 'postgresql://{}:{}@localhost:5432/casting'.format(DB_USER, DB_PASS)
    yield client

def test_get_actors(client):
    length = len(Actor.query.all())
    res = client.get('/actors', headers=EXECUTIVE_PRODUCER_HEADER)
    data = json.loads(res.data)
    
    assert res.status_code == 200
    assert len(data['actors']) == length

def test_get_actors_no_authorization(client):
    res = client.get('/actors')
    
    assert res.status_code == 401

def test_get_movies(client):
    length = len(Movie.query.all())
    res = client.get('/movies', headers=EXECUTIVE_PRODUCER_HEADER)
    data = json.loads(res.data)
    
    assert res.status_code == 200
    assert len(data['movies']) == length

def test_get_movies_no_authorization(client):
    res = client.get('/movies')
    
    assert res.status_code == 401

def test_post_actor(client):
    prev_length = len(Actor.query.all())
    new_actor = {'name': 'Bad Actor', 'age': 89, 'gender': 'male'}
    res = client.post('/actors', headers=EXECUTIVE_PRODUCER_HEADER, json=new_actor)
    data = json.loads(res.data)

    assert res.status_code == 200
    assert len(Actor.query.all()) == prev_length + 1

def test_post_actor_malformed(client):
    new_actor = {'name': 'Bad Actor', 'gender': 'male'}
    res = client.post('/actors', headers=EXECUTIVE_PRODUCER_HEADER, json=new_actor)

    assert res.status_code == 400

def test_post_movie(client):
    prev_length = len(Movie.query.all())
    new_movie = {'title': 'Bad Movie', 'release': datetime.now()}
    res = client.post('/movies', headers=EXECUTIVE_PRODUCER_HEADER, json=new_movie)
    data = json.loads(res.data)

    assert res.status_code == 200
    assert len(Movie.query.all()) == prev_length + 1

def test_post_movie_malformed(client):
    new_movie = {'title': 'Bad Movie'}
    res = client.post('/movies', headers=EXECUTIVE_PRODUCER_HEADER, json=new_movie)
    
    assert res.status_code == 400

def test_delete_actor(client):
    actor = Actor(name='new actor', age=33, gender='female')
    actor.insert()
    prev_length = len(Actor.query.all())

    res = client.delete('/actors/{}'.format(actor.id), headers=EXECUTIVE_PRODUCER_HEADER)

    assert res.status_code == 200
    assert len(Actor.query.all()) == prev_length - 1

def test_delete_actor_nonexistent(client):
    res = client.delete('/actors/{}'.format(99999), headers=EXECUTIVE_PRODUCER_HEADER)
    
    assert res.status_code == 404

def test_delete_movie(client):
    movie = Movie(title='new movie', release=datetime.now())
    movie.insert()
    prev_length = len(Movie.query.all())

    res = client.delete('/movies/{}'.format(movie.id), headers=EXECUTIVE_PRODUCER_HEADER)

    assert res.status_code == 200
    assert len(Movie.query.all()) == prev_length - 1

def test_delete_movie_nonexistent(client):
    res = client.delete('/movies/{}'.format(99999), headers=EXECUTIVE_PRODUCER_HEADER)
    
    assert res.status_code == 404

def test_patch_actor(client):
    actor = Actor(name='actor', age=25, gender='female')
    actor.insert()
    actor_id = actor.id
    updated_actor = {'name': 'actor', 'age': 26, 'gender': 'female'}
    res = client.patch('/actors/{}'.format(actor_id), headers=EXECUTIVE_PRODUCER_HEADER, json=updated_actor)
    
    actor = Actor.query.filter(Actor.id == actor_id).first()
    assert res.status_code == 200
    assert actor.name == 'actor' and actor.age == 26 and actor.gender == 'female'

def test_patch_actor_nonexistent(client):
    updated_actor = {'name': 'actor', 'age': 26, 'gender': 'female'}
    res = client.patch('/actors/{}'.format(99999), headers=EXECUTIVE_PRODUCER_HEADER, json=updated_actor)

    assert res.status_code == 404

def test_patch_movie(client):
    release = datetime.now()
    movie = Movie(title='movie', release=release)
    movie.insert()
    movie_id = movie.id
    updated_movie = {'title': 'updated movie name', 'release': release}
    res = client.patch('/movies/{}'.format(movie_id), headers=EXECUTIVE_PRODUCER_HEADER, json=updated_movie)
    
    movie = Movie.query.filter(Movie.id == movie_id).first()
    assert res.status_code == 200
    assert movie.title == 'updated movie name'

def test_patch_movie_nonexistent(client):
    release = datetime.now()
    updated_movie = {'title': 'updated movie name', 'release': release}
    res = client.patch('/movies/{}'.format(99999), headers=EXECUTIVE_PRODUCER_HEADER, json=updated_movie)
    
    assert res.status_code == 404

def test_get_actors_assistant(client):
    length = len(Actor.query.all())
    res = client.get('/actors', headers=CASTING_ASSISTANT_HEADER)
    data = json.loads(res.data)
    
    assert res.status_code == 200
    assert len(data['actors']) == length

def test_delete_actor_assistant(client):
    res = client.delete('/actors/{}'.format(1), headers=CASTING_ASSISTANT_HEADER)

    assert res.status_code == 401

def test_delete_actor_director(client):
    actor = Actor(name='new actor', age=33, gender='female')
    actor.insert()
    prev_length = len(Actor.query.all())
    
    res = client.delete('/actors/{}'.format(actor.id), headers=CASTING_DIRECTOR_HEADER)
    
    assert res.status_code == 200
    assert len(Actor.query.all()) == prev_length - 1

def test_delete_movie_director(client):
    res = client.delete('/movies/{}'.format(1), headers=CASTING_DIRECTOR_HEADER)

    assert res.status_code == 401



if __name__ == "__main__":
  unittest.main()
