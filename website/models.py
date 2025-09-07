from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)

    last_name = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(50))
    location = db.Column(db.String(150))
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    notes = db.relationship('Note', backref='user', lazy=True)
