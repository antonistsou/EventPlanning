from . import db
from flask_login import UserMixin


# User db scheme
class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(150), unique = True)
    firstName = db.Column(db.String(150))
    password = db.Column(db.String(150))

# Events db sceme 
class Events():
    id= db.Column(db.Integer , primary_key = True)