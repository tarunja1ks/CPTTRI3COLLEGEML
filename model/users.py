""" database dependencies to support sqlite examples """
import datetime
from datetime import datetime
import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into a Python shell and follow along '''

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    _role = db.Column(db.String(20), default="User", nullable=False)
    _email = db.Column(db.String(255), unique=False, nullable=False)
    _college_list = db.Column(db.String(255), unique=False, nullable=False, default='[]')


    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, email, password="123qwerty", dob=datetime.today(), role="User", college_list=[]):
        self._name = name
        self._uid = uid
        self.set_password(password)
        if isinstance(dob, str):  # not a date type     
            dob = date=datetime.today()
        self._dob = dob
        self._email = email
        self._role = role
        self._college_list = college_list

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # intializing user data 
    @classmethod
    def initUsers(cls):
        """Initialize sample users."""
        try:
            # Check if any users exist
            existing_users = cls.query.all()
            if not existing_users:
                # Only add sample users if no users exist
                u1 = cls(name='Thomas Edison', uid='toby', email="123@123.com", password='123toby', dob=datetime(1847, 2, 11), role='Admin')
                u2 = cls(name='Nikola Tesla', uid='niko', email="123@123.com", password='123niko', role='User')
                u3 = cls(name='Alexander Graham Bell', uid='lex', email="123@123.com", password='123lex', role='User')
                u4 = cls(name='Eli Whitney', uid='whit', email="123@123.com", password='123whit', role='User')
                u5 = cls(name='Indiana Jones', uid='indi', email="123@123.com", dob=datetime(1920, 10, 21), role='User')
                u6 = cls(name='Marion Ravenwood', uid='raven', email="123@123.com", dob=datetime(1921, 10, 21), role='User')

                users = [u1, u2, u3, u4, u5, u6]

                # Add each user to the database
                for user in users:
                    db.session.add(user)

                # Commit changes to the database
                db.session.commit()

        except IntegrityError:
            # Handle IntegrityError if there is an issue
            db.session.remove()
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts uid from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows uid to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # a setter property for role
    @property
    def role(self):
        return self._role
    
    @role.setter
    def role(self, role):
        self._role = role
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    def is_admin(self):
        return self._role == "Admin"
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional method used for setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, method="pbkdf2:sha256")

    # check password parameter against stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # dob property is returned as string, a string represents date outside object
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob setter, verifies date type before it is set or default to today
    @dob.setter
    def dob(self, dob):
        if isinstance(dob, str):  # not a date type     
            dob = date=datetime.today()
        self._dob = dob
                
    # a email getter method, extracts email from object
    @property
    def email(self):
        return self._email
    
    # a setter function, allows email to be updated after initial object creation
    @email.setter
    def email(self, email):
        self._email = email
        
    @property
    def college_list(self):
        return self._college_list
    
    @college_list.setter
    def college_list(self, college_list):
        self._college_list = college_list
    
    # age is calculated field, age is returned according to date of birth
    @property
    def age(self):
        today = datetime.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
    
    # output content using str(object) is in human readable form
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
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
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "dob": self.dob,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "colleges": self.college_list
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password="",email=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if len(email) > 0:
            self.email = email
        db.session.add(self) # performs update when id exists
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None