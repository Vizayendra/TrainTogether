from flask import Blueprint, render_template, abort
from flask_login import login_required
from .models import User

main = Blueprint('main', __name__)

@main.route('/partner/<int:user_id>')
@login_required
def partner_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    return render_template('partner_profile.html', user=user)
