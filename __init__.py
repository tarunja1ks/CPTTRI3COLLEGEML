
"""
These imports define the key objects
"""

import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

"""
These object and definitions are used throughout the Jupyter Notebook.
"""

# Setup of key Flask object (app)
app = Flask(__name__)
# Setup SQLAlchemy object and properties for the database (db)
database = 'sqlite:///sqlite.db'  # path and filename of database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.logger.setLevel(logging.INFO)
app.logger.addHandler(logging.StreamHandler())  # Logs to console
db = SQLAlchemy()


# This belongs in place where it runs once per project
db.init_app(app)