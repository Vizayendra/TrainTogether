from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
<<<<<<< HEAD
from flask_login import LoginManager
=======
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
<<<<<<< HEAD
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

=======
    app.config['SECRET_KEY'] = 'dfdfdffd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(path.dirname(__file__), DB_NAME)}'
    db.init_app(app)


>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

<<<<<<< HEAD
    from .models import User, Note, Workout, seed_workouts

    with app.app_context():
        db.create_all()
        seed_workouts()  # auto-fill workouts
=======
    from .models import User

    create_database(app)
>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

<<<<<<< HEAD
=======
        from flask_login import current_user
    @app.context_processor
    def inject_user():
        return dict(user=current_user)

>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4
    return app


def create_database(app):
<<<<<<< HEAD
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
=======
    db_path = path.join(path.dirname(__file__), DB_NAME)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
            print(f'Created Database at {db_path}')
>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4
