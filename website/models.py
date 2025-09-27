# website/models.py

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path # Keep this if create_database_and_seed is still used here

# Association table for many-to-many (users ↔ workouts)
user_workouts = db.Table(
    'user_workouts',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(150))
    bio = db.Column(db.String(500), default="Hello, I am new here!")
    phone_number = db.Column(db.String(11), nullable=True)
    activity_types = db.Column(db.String(200), default="", nullable=True)
    
    workouts = db.relationship('Workout', secondary=user_workouts, backref='users', lazy='dynamic')
    
    partner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # --- FIX: ADDING post_update=True ---
    partner = db.relationship(
        'User', 
        remote_side=[id], 
        backref='partner_of', 
        uselist=False,
        post_update=True  # This resolves the CircularDependencyError
    )

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# NOTE: I am including the helper functions below based on your previous complete files, 
# assuming they are still needed for database creation/seeding.

def seed_workouts():
    default_workouts = ["Cardio", "Strength Training", "Yoga", "HIIT", "Flexibility", "Endurance"]
    for w in default_workouts:
        if not Workout.query.filter_by(name=w).first():
            db.session.add(Workout(name=w))
    db.session.commit()

def create_database_and_seed():
    DB_NAME = "database.db"
    if not path.exists('instance/' + DB_NAME):
        db.create_all()
        print('Created Database!')
        seed_workouts()
        print('Seeded Workouts!')