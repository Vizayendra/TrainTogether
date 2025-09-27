# website/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'saadadafsfc'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .models import User, Note, Workout
    from .views import views
    from .auth import auth

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def seed_workouts():
        default_workouts = ["Cardio", "Strength Training", "Yoga", "HIIT", "Flexibility", "Endurance"]
        for w in default_workouts:
            if not Workout.query.filter_by(name=w).first():
                db.session.add(Workout(name=w))
        db.session.commit()

    def create_database():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print('Created Database!')
            seed_workouts()
            print('Seeded Workouts!')

    with app.app_context():
        create_database()

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app