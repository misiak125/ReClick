from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from .models import User
from . import db
from flask_mailman import EmailMessage
from .utils.decorators import active_login_required
from .forms import SearchUserForm

views=Blueprint('views', __name__)
usersbp=Blueprint('users', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/profile')
@active_login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@views.route('/users', methods=['GET', 'POST'])
def users():
    form = SearchUserForm(request.form)
    if request.method == 'POST':
        username = form.search.data
        if username:
            users = User.query.filter(User.name.like(f'%{username}%')).filter_by(is_confirmed=True).all()
        else:
            users = User.query.filter_by(is_confirmed=True).all()
    else:
        users = User.query.filter_by(is_confirmed=True).all()
    return render_template('users.html', users=users, form=form)

@views.route('/play')
def play():
    return render_template('game.html')

@views.route("/user/<int:userid>")
def userpage(userid):
    user = User.query.get(userid)
    game_count = 69
    high_score = 2137

    if user is None or not user.is_confirmed:
        abort(404)
        
    return render_template('userpage.html', user=user, high_score=high_score, game_count=game_count)