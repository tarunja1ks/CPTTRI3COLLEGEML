""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class College(db.Model):
    __tablename__ = 'colleges'  # table name is plural, class name is singular

    # Define the Player schema with "vars" from object
    _name = db.Column(db.String(255), unique=True, nullable=False)
    _link = db.Column(db.String(255), unique=True, nullable=False)
    _type = db.Column(db.String(255), unique=False, nullable=True)

    # constructor of a Player object, initializes the instance variables within object (self)
    def __init__(self, name, link, type):
        self._name = name    # variables with self prefix become part of the object, 
        self._link = link
        self.type = type

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def link(self):
        return self._link
    
    @name.setter
    def name(self, link):
        self._link = link
        
    @property
    def type(self):
        return self._type
    
    @name.setter
    def name(self, type):
        self._type = type
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a player object from Player(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "name": self.name,
            "link": self.link,
            "type": self.type
        }

    # CRUD update: updates name, uid, password, tokens
    # returns self
    def update(self, dictionary):
        """only updates values in dictionary with length"""
        for key in dictionary:
            if key == "name":
                self.name = dictionary[key]
            if key == "link":
                self.link = dictionary[key]
            if key == "type":
                self.type = dictionary[key]
        db.session.commit()
        return self

    # CRUD delete: remove self
    # return self
    def delete(self):
        colleges = self
        db.session.delete(self)
        db.session.commit()
        return colleges


"""Database Creation and Testing """


# Builds working data for testing
def initPlayers():
    with app.app_context():
        db.create_all()
        colleges = [
            College() #FILL OUT THIS WHEN POSSIBLE
        ]

        """Builds sample user/note(s) data"""
        for college in colleges:
            try:
                college.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {college.name}")