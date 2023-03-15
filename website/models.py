from . import db
from flask_login import UserMixin

# User db scheme
class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(150), unique = True)
    firstName = db.Column(db.String(150))
    password = db.Column(db.String(150))
    result = db.relationship('Result')

class Event(db.Model):
    id = db.Column(db.Integer , primary_key =True)
    link = db.Column(db.String(150) , unique = True)
    name = db.Column(db.String(1000))
    image = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    info = db.Column(db.String(1000))
    location = db.Column(db.String(1000))
    dates = db.relationship('Date')
 
class Date(db.Model):
    date_id = db.Column(db.Integer , primary_key =True)
    dayname= db.Column(db.String(2))
    day = db.Column(db.Date)
    time = db.Column(db.String(32))
    event_id = db.Column(db.Integer , db.ForeignKey('event.id'))
 
class Result(db.Model):
    id = db.Column(db.Integer , primary_key = True )
    result = db.Column(db.String(100000))
    user_id =db.Column(db.Integer , db.ForeignKey('user.id'))
