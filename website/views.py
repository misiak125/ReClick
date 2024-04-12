from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import User
from . import db
from .forms import SearchUserForm

views=Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@views.route('/users', methods=['GET', 'POST'])
def users():
    form = SearchUserForm(request.form)
    if request.method == 'POST':
        username = form.search.data
        if username:
            users = User.query.filter(User.name.like(f'%{username}%')).all()
        else:
            users = User.query.all()
    else:
        users = User.query.all()
    return render_template('users.html', users=users, form=form)
