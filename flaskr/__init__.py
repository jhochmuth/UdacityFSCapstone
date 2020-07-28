import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from ..models import db, setup_db, Actor, Movie
from ..auth.auth import AuthError, requires_auth


def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE')
    return response

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(jwt):
    actors = Actor.query.all()
    actors = [actor.format() for actor in actors]

    return jsonify({'success': True, 'actors': actors})

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(jwt):
    movies = Movie.query.all()

    movies = [movie.format() for movie in movies]

    return jsonify({'success': True, 'movies': movies})

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actor(jwt):
    try:
      data = request.get_json()
      actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
          
      actor.insert()
    except:
      abort(400)
                                      
    return jsonify({'success': True})
                    
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def post_movie(jwt):
    try:
      data = request.get_json()
      movie = Movie(title=data['title'], release=data['release'])
    
      movie.insert()
    except:
      abort(400)
  
    return jsonify({'success': True})

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
    actor = Actor.query.filter_by(id=actor_id).first()

    if actor is None:
      abort(404)

    actor.delete()
    return jsonify({'success': True})

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()

    if movie is None:
      abort(404)
    
    movie.delete()
    return jsonify({'success': True})

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def patch_actor(jwt, actor_id):
    data = request.get_json()
    actor = Actor.query.filter_by(id=actor_id).first()

    if actor is None:
      abort(404)
    
    try:
      actor.name = data['name']
      actor.age = data['age']
      actor.gender = data['gender']
      actor.update()

    except:
      abort(400)

    return jsonify({'success': True})

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def patch_movie(jwt, movie_id):
    data = request.get_json()
    movie = Movie.query.filter_by(id=movie_id).first()

    if movie is None:
      abort(404)
          
    try:
      movie.title = data['title']
      movie.release = data['release']
      movie.update()

    except:
      abort(400)

    return jsonify({'success': True})

  @app.errorhandler(AuthError)
  def unauthorized_request(error):
    return jsonify({
      "success": False,
      "error": 401,
      "message": "Unauthorized request."
    }), 401

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': "Bad request."
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "Page not found."
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "Unprocessable entity."
    }), 422

  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': "Internal server error."
    }), 500

  return app
