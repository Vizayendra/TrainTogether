from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

# Landing page 
@views.route('/')
def landing():
    if current_user.is_authenticated:
        # If user is already logged in, go to home page
        return render_template('home.html', user=current_user)
    else:
        # If not, show landing page
        return render_template("landing.html")

# Home page
@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

# Profile page
@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        bio = request.form.get('bio')
        phone_number = request.form.get("phone_number")
        current_user.bio = bio
        current_user.phone_number = phone_number
        db.session.commit()
        flash('Profile updated!', category='success')

    return render_template("profile.html", user=current_user)
