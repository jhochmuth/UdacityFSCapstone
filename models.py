import os
from sqlalchemy import Column, String, DateTime, Integer, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.urandom(24)
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.create_all()

class Movie(db.Model):
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release = Column(DateTime)

  def __init__(self, title, release):
    self.title = title
    self.release = release

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release': self.release
    }

class Actor(db.Model):
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender
  
  def insert(self):
      db.session.add(self)
      db.session.commit()
  
  def update(self):
      db.session.commit()
  
  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }
