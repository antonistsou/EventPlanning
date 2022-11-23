from . import db
from flask_login import UserMixin
from bs4 import BeautifulSoup


# User db scheme
class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(150), unique = True)
    firstName = db.Column(db.String(150))
    password = db.Column(db.String(150))

class Event:
    def __init__(self, id, name, image, description, location , day , time ):
        self.id=id
        self.name = name
        self.image = image
        self.description = description
        self.location = location
        self.day = day 
        self.time = time

    

