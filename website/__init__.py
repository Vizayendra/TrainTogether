from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    
    # App configuration
    app.config['SECRET_KEY'] = 'dfdfdffd'  # ⚠️ Better to use env variable
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{path.join(path.dirname(__file__), DB_NAME)}"
    
    # Mail configuration (only if using Flask-Mail)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@gmail.com'          # ⚠️ Replace with your email
    app.config['MAIL_PASSWORD'] = 'your-app-password'             # ⚠️ Use Gmail App Password
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models (without Note!)
    from .models import User, Message, Activity  

    create_database(app)

    # Login Manager setup
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    db_path = path.join(path.dirname(__file__), DB_NAME)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
            print(f'✅ Created database at {db_path}')
