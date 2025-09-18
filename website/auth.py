<<<<<<< HEAD
# In website/auth.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Workout  # <-- THE FIX IS HERE
=======
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

<<<<<<< HEAD

=======
>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4
@auth.route('/logout')
@login_required
def logout():
    logout_user()
<<<<<<< HEAD
    return redirect(url_for('auth.login'))
=======
    return redirect(url_for('views.landing'))
>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
<<<<<<< HEAD
        password = request.form.get('password')
        password2 = request.form.get('password2')
        selected_workout_ids = request.form.getlist('workouts')
=======
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
<<<<<<< HEAD
        elif password != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            # I've updated this to 'pbkdf2:sha256' as it's more secure than 'sha256'
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, method='pbkdf2:sha256'))

            # Add selected workouts to the user
            for workout_id in selected_workout_ids:
                workout = Workout.query.get(int(workout_id))
                if workout:
                    new_user.workouts.append(workout)

=======

        # To make sure the data entered is valid
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')  
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

<<<<<<< HEAD
    # Get all workouts to display on the sign-up form
    all_workouts = Workout.query.all()
    return render_template("sign_up.html", user=current_user, all_workouts=all_workouts)

=======
    return render_template("sign_up.html", user=current_user)
>>>>>>> 52f7f308b51553a79ba653d24b23c08003eb6ea4
