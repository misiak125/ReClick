from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from flask_mailman import EmailMessage
from .utils.decorators import active_login_required

views=Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/profile')
@active_login_required
def profile():
    return render_template('profile.html', name=current_user.name)


