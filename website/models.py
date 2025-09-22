from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(150))
    bio = db.Column(db.String(500), default="Hello, I am new here!")
    phone_number = db.Column(db.String(11), nullable=True)
    email = db.Column(db.String(150), unique=True)
    activity_types = db.Column(db.String(200), default="", nullable=True)

    # relationship to Activity table
    activities = db.relationship('Activity', backref='owner', lazy=True)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))              
    email = db.Column(db.String(150))            
    phone_number = db.Column(db.String(11))       
    activity_type = db.Column(db.String(50))      
    upcoming = db.Column(db.String(200), default="Coming soon...")  

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)