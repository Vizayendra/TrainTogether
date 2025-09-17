print("==> views.py: Loaded")

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Message, User
from .forms import MessageForm
from . import db
import json

views = Blueprint('views', __name__)

# ------------------ Home Route ------------------ #
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if not note or len(note.strip()) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note.strip(), user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

# ------------------ Delete Note ------------------ #
@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note_data = json.loads(request.data)
    note_id = note_data.get('noteId')
    note = Note.query.get(note_id)

    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"success": True})

    return jsonify({"success": False, "error": "Unauthorized or note not found"})

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