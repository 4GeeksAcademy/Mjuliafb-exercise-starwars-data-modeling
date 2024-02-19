import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Character(Base):
    __tablename__ = "character"
    character_id = Column(Integer, primary_key=True)
    gender = Column(String(40))
    name = Column(String(40), unique=True, nullable=False)
    film_id = Column(Integer, nullable=False)
    homeworld_id = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "character_id": self.character_id,
            "name": self.name,
            "gender": self.gender,
            "film_id" : self.film_id,
            "homeworld_id": self.homeworld_id,
        }

class Planet(Base):
    __tablename__ = "planet"
    planet_id = Column(Integer, primary_key=True)
    climate = Column(String(200))
    name = Column(String(40), nullable=False)
    resident_id = Column(Integer,ForeignKey('character.character_id') ,nullable=False)
    character= relationship(Character)
    film_id = Column(Integer,nullable=False) 

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "planet_id": self.planet_id,
            "name": self.name,
            "climate": self.climate,
            "film_id" : self.film_id,
            "resident_id": self.resident_id,
        }

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=True)
    password = Column(String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
            # do not serialize the password, its a security breach
        }

class Favorites(Base):
   __tablename__ = "favorite"
   id = Column(Integer, primary_key=True)
   user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
   user = relationship(User)
   character_id = Column(Integer,ForeignKey('character.character_id'), nullable=True)
   character = relationship(Character)
   planet_id = Column(Integer, ForeignKey('planet.planet_id'), nullable=True)
   planet = relationship(Planet)

   def __repr__(self):
        return '<Favorite %r>' % self.id

   def serialize(self):
        if self.character_id is not None:
            fav_type = "character"
            fav_id = self.character_id
        elif self.planet_id is not None:
            fav_type = "planet"
            fav_id = self.planet_id
        else:
            fav_type = "unknown"
            fav_id = None    
        return {
            "id": self.id,
            "user_id": self.user_id,
            "fav_type": fav_type,
            "fav_id": fav_id,
        }

class Film(Base):
    __tablename__ = "film"
    film_id = Column(Integer, primary_key=True)
    character_id = Column(Integer,ForeignKey('character.character_id') ,nullable=False)
    character = relationship(Character)
    planet_id = Column(Integer, ForeignKey('planet.planet_id') ,nullable=False)
    planet = relationship(Planet)
    director = Column(String(40), nullable=False)
    title = Column(String(200), nullable=False)

    def __repr__(self):
        return '<Film %r>' % self.title

    def serialize(self):
        return {
            "film_id": self.film_id,
            "title": self.title,
            "director" : self.director,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
