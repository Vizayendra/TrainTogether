from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import MessageForm, ActivityForm
from . import db
from .models import User, Activity, Message

views = Blueprint('views', __name__)

# Landing page 
@views.route('/')
def landing():
    if current_user.is_authenticated:
        return render_template('home.html', user=current_user)
    else:
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
        activities = request.form.getlist('activities') 

        if len(activities) > 3:
            flash("You can only select up to 3 activities.", category="error")
            return render_template("profile.html", user=current_user)

        current_user.bio = bio
        current_user.phone_number = phone_number
        current_user.activity_types = ",".join(activities)
        db.session.commit()
        flash('Profile updated!', category='success')
        return redirect("/profile")

    return render_template("profile.html", user=current_user)

# Messages page
@views.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    form = MessageForm()
    form.receiver.choices = [(u.id, u.email) for u in User.query.order_by(User.email).all() if u.id != current_user.id]

    if form.validate_on_submit():
        msg = Message(
            content=form.content.data,
            sender_id=current_user.id,
            receiver_id=form.receiver.data
        )
        db.session.add(msg)
        db.session.commit()
        flash('Message sent!', 'success')
        return redirect(url_for('views.messages'))

    inbox = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.timestamp.desc()).all()
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.timestamp.desc()).all()

    return render_template('messages.html', form=form, inbox=inbox, sent=sent)

# Activity table
@views.route('/activity')
@login_required  
def activity_page():
    users = User.query.all()
    activities = Activity.query.all()
    form = ActivityForm()
    return render_template("activity.html", users=users, activities=activities, form=form)

# Add activity 
@views.route('/add-activities', methods=['GET','POST'])
@login_required
def add_activity_page():
    form = ActivityForm()
    if form.validate_on_submit():  # Only runs when user clicks Submit
        new_activity = Activity(
            activity_type=form.activity_type.data,
            date=form.date.data,
            time=form.time.data,
            location=form.location.data,
            user_id=current_user.id
        )
        db.session.add(new_activity)
        db.session.commit()
        flash('Activity added!', 'success')
        return redirect(url_for('views.activity_page'))  # Go back to main activity page
    # If GET request or form fails, just show the form again
    return render_template('add_activity.html', form=form)