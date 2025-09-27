# website/views.py

import random
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Note, Workout, db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    # 1. Define a list of random fitness facts
    fitness_facts = [
        "Exercise can improve your mood and reduce feelings of depression and anxiety.",
        "Staying hydrated is crucial for maintaining energy levels and brain function.",
        "Strength training can boost your metabolism, helping you burn more calories throughout the day.",
        "Getting enough quality sleep is as important for your health as nutrition and exercise.",
        "On average, a person walks about 70,000 miles in their lifetime - that's like walking around the world almost three times!",
        f"Hey {current_user.first_name}, did you know consistency is more important than intensity? Keep up the great work!"
    ]
    random_fact = random.choice(fitness_facts)

    # 2. Get all workouts to display in the dropdown and accordion
    all_workouts = Workout.query.order_by(Workout.name).all()

    # 3. For each workout, get a few users who have selected it
    users_by_workout = {}
    for workout in all_workouts:
        # Query for users who have this workout, are not the current user, and do not have a partner
        users = User.query.filter(
            User.workouts.any(Workout.id == workout.id),
            User.id != current_user.id,
            User.partner_id.is_(None)
        ).limit(4).all()
        users_by_workout[workout.id] = users

    return render_template(
        "home.html",
        user=current_user,
        random_fact=random_fact,
        all_workouts=all_workouts,
        users_by_workout=users_by_workout
    )


@views.route('/workouts', methods=['GET', 'POST'])
@login_required
def workouts():
    # Get all workouts for the dropdown menu
    all_workouts = Workout.query.order_by(Workout.name).all()
    
    if request.method == 'POST':
        # Get the workout ID from the form submission
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


@views.route('/search')
@login_required
def search():
    workout_id = request.args.get('workout_id')
    users_found = []
    workout_name = "All Workouts"

    if workout_id:
        selected_workout = Workout.query.get(workout_id)
        if selected_workout:
            workout_name = selected_workout.name
            users_found = User.query.filter(
                User.workouts.any(Workout.id == selected_workout.id),
                User.id != current_user.id,
                User.partner_id.is_(None)
            ).all()
        else:
            flash("Selected workout not found.", category="error")
    
    return render_template("search_results.html", user=current_user, users_found=users_found, query=workout_name)


@views.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user_profile = User.query.get_or_404(user_id)
    
    suggested_partners = []
    if user_profile.id == current_user.id:
        user_workout_ids = [w.id for w in current_user.workouts]
        if user_workout_ids:
            suggested_partners = User.query.join(User.workouts).filter(
                Workout.id.in_(user_workout_ids),
                User.id != current_user.id,
                User.partner_id.is_(None)
            ).distinct().limit(5).all()

    return render_template("profile.html", user=current_user, user_profile=user_profile, suggested_partners=suggested_partners)


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
        partner_to_add.partner = current_user
        db.session.commit()
        flash(f'{partner_to_add.first_name} is now your workout partner!', category='success')
    
    return redirect(url_for('views.profile', user_id=current_user.id))


@views.route('/remove-partner', methods=['POST'])
@login_required
def remove_partner():
    if current_user.partner:
        partner_name = current_user.partner.first_name
        partner_to_remove = current_user.partner
        
        current_user.partner = None
        partner_to_remove.partner = None
        
        db.session.commit()
        flash(f'{partner_name} has been removed as your partner.', category='success')
    else:
        flash('You do not have a partner to remove.', category='error')
    
    return redirect(url_for('views.profile', user_id=current_user.id))