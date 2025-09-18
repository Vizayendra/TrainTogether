

import random # <--- ADD THIS LINE
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note, Workout
from . import db
from sqlalchemy import or_
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    # 1. Define some random fitness facts
    fitness_facts = [
        "Exercise can improve your mood and reduce feelings of depression and anxiety.",
        "Staying hydrated is crucial for maintaining energy levels and brain function.",
        "Strength training can boost your metabolism, helping you burn more calories throughout the day.",
        "Getting enough quality sleep is as important for your health as nutrition and exercise.",
        "On average, a person walks about 70,000 miles in their lifetime - that's like walking around the world almost three times!",
        f"Hey {current_user.first_name}, did you know consistency is more important than intensity? Keep up the great work!"
    ]
    random_fact = random.choice(fitness_facts) # This line will now work

    # 2. Get all workouts to display on the page
    all_workouts = Workout.query.order_by(Workout.name).all()

    # 3. For each workout, get a few users who have selected it
    users_by_workout = {}
    for workout in all_workouts:
        users = User.query.filter(
            User.workouts.contains(workout), 
            User.id != current_user.id,
            User.partner_id == None
        ).limit(4).all()
        users_by_workout[workout.id] = users

    return render_template(
        "home.html", 
        user=current_user, 
        random_fact=random_fact, 
        all_workouts=all_workouts,
        users_by_workout=users_by_workout
    )
    return render_template(
        "home.html", 
        user=current_user, 
        random_fact=random_fact, 
        all_workouts=all_workouts,
        users_by_workout=users_by_workout
    )
# ... (keep your existing workouts, remove_workout, and delete_note routes)
@views.route('/workouts', methods=['GET', 'POST'])
@login_required
def workouts():
    all_workouts = Workout.query.all()
    if request.method == 'POST':
        workout_id = request.form.get('workout_id')
        workout = Workout.query.get(workout_id)

        if workout:
            if workout not in current_user.workouts:
                current_user.workouts.append(workout)
                db.session.commit()
                flash(f"{workout.name} added to your plan!", category="success")
            else:
                flash(f"{workout.name} is already in your plan.", category="info")
        return redirect(url_for('views.workouts'))

    return render_template("workouts.html", user=current_user, workouts=all_workouts)

@views.route('/remove-workout/<int:workout_id>', methods=['POST'])
@login_required
def remove_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if workout and workout in current_user.workouts:
        current_user.workouts.remove(workout)
        db.session.commit()
        flash(f"{workout.name} removed from your plan.", category="info")
    return redirect(url_for('views.workouts'))

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return jsonify({})


# --- NEW AND UPDATED ROUTES BELOW ---

# In website/views.py

# ... (imports and other routes remain the same) ...

# UPDATED: Route for handling user searches from the dropdown
@views.route('/search')
@login_required
def search():
    workout_id = request.args.get('workout_id')
    users_found = []
    workout_name = "all workouts" # Default search term display

    if workout_id:
        # Find the selected workout object
        selected_workout = Workout.query.get(workout_id)
        if selected_workout:
            workout_name = selected_workout.name
            # Find all users who have this workout, excluding the current user
            users_found = User.query.filter(
                User.workouts.contains(selected_workout),
                User.id != current_user.id
            ).all()
        else:
            flash("Selected workout not found.", category="error")
    
    return render_template("search_results.html", user=current_user, users_found=users_found, query=workout_name)

# ... (The rest of your views.py file can remain the same) ...

# UPDATED: Profile route to show partners and suggestions
@views.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user_profile = User.query.get_or_404(user_id)
    
    suggested_partners = []
    # Only generate suggestions if viewing your own profile
    if user_profile.id == current_user.id:
        user_workout_ids = [w.id for w in current_user.workouts]
        if user_workout_ids:
            # Find users who share at least one workout, are not the current user, and don't already have a partner
            suggested_partners = User.query.join(User.workouts).filter(
                Workout.id.in_(user_workout_ids),
                User.id != current_user.id,
                User.partner_id == None
            ).distinct().limit(5).all()

    return render_template("profile.html", user=current_user, user_profile=user_profile, suggested_partners=suggested_partners)

# NEW: Route to add a workout partner
@views.route('/add-partner/<int:partner_id>', methods=['POST'])
@login_required
def add_partner(partner_id):
    partner_to_add = User.query.get(partner_id)
    if not partner_to_add:
        flash('User not found.', category='error')
    elif partner_to_add.id == current_user.id:
        flash('You cannot add yourself as a partner.', category='error')
    elif current_user.partner:
        flash('You already have a workout partner. Remove your current partner first.', category='error')
    else:
        current_user.partner = partner_to_add
        db.session.commit()
        flash(f'{partner_to_add.first_name} is now your workout partner!', category='success')
    
    return redirect(url_for('views.profile', user_id=current_user.id))

# NEW: Route to remove a workout partner
@views.route('/remove-partner', methods=['POST'])
@login_required
def remove_partner():
    if current_user.partner:
        partner_name = current_user.partner.first_name
        current_user.partner = None
        db.session.commit()
        flash(f'{partner_name} has been removed as your partner.', category='success')
    else:
        flash('You do not have a partner to remove.', category='error')
    
    return redirect(url_for('views.profile', user_id=current_user.id))
