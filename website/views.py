print("==> views.py: Loaded")

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Message, User, Activity
from .forms import MessageForm, ActivityForm   # ✅ include ActivityForm
from . import db
import json


views = Blueprint('views', __name__)

# ------------------ Home Route ------------------ #
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

# ------------------ Contact Form ------------------ #
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
 
@views.route('/activities', methods=['GET', 'POST'])
@login_required
def activities():
    form = ActivityForm()
    if form.validate_on_submit():
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
        return redirect(url_for('views.activities'))

    # show all activities (newest first)
    activities = Activity.query.order_by(Activity.date.desc(), Activity.time.desc()).all()
    return render_template('activities.html', form=form, activities=activities, user=current_user)
