from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User
from . import db

views=Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@views.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
