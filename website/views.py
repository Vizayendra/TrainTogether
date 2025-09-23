from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .forms import MessageForm

from . import db
from .models import User
from .models import User, Activity, Message


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
        activities = request.form.getlist('activities') 

        # limited to 3 activities
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
    # Fill dropdown with all users except yourself
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

    # show messages for the logged-in user
    inbox = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.timestamp.desc()).all()
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.timestamp.desc()).all()

    return render_template('messages.html', form=form, inbox=inbox, sent=sent)

# Activity page
@views.route('/activity')
@login_required  
def activity():
    users = User.query.all()
    return render_template("activity.html", users=users)


# Add Activity page (temporary placeholder)
@views.route('/add-activity')
@login_required
def add_activity():
    return "<h1>Add Activity Page</h1>"
