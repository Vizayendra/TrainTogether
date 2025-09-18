from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

<<<<<<< HEAD
# Association table for many-to-many (users ↔ workouts)
user_workouts = db.Table(
    'user_workouts',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id'))
)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# In website/models.py

# ... (keep everything else the same)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)

    # New: relationship with workouts
    workouts = db.relationship('Workout', secondary=user_workouts, backref='users', lazy='dynamic')

    # ADD THESE TWO LINES for the partner relationship
    partner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    partner = db.relationship('User', remote_side=[id], backref='partner_of', uselist=False)

# ... (rest of the file is the same)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


# Function to auto-seed workouts if empty
def seed_workouts():
    default_workouts = ["Cardio", "Strength Training", "Yoga", "HIIT", "Flexibility", "Endurance"]
    for w in default_workouts:
        if not Workout.query.filter_by(name=w).first():
            db.session.add(Workout(name=w))
    db.session.commit()

=======

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(150))
    bio = db.Column(db.String(500), default="Hello, I am new here!")
    phone_number = db.Column(db.String(11), nullable=True)
    activity_types = db.Column(db.String(200), default="", nullable=True)
>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4

