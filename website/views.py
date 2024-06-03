from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from .models import User
from . import db
from flask_mailman import EmailMessage
from flask_login import current_user
from .utils.decorators import active_login_required
from .forms import SearchUserForm
from datetime import datetime
from .models import Comment
from .forms import CommentForm

views=Blueprint('views', __name__)
usersbp=Blueprint('users', __name__)

@views.route('/')
def index():
    return render_template('index.html')

#@views.route('/profile')
#@active_login_required
#def profile():
#    return render_template('profile.html', name=current_user.name)


@views.route('/users', methods=['GET', 'POST'])
@active_login_required
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

@views.route("/user/<int:userid>", methods=['GET', 'POST'])
@active_login_required
def userpage(userid):
    user = User.query.get(userid)
    game_count = 69
    high_score = 2137

    if user is None or not user.is_confirmed:
        abort(404)
        
    user_comments = Comment.query.filter_by(user_to_id=user.id)
    comment_form = CommentForm()
    if request.method == 'POST':
        print("testestdf1")
    if request.method == 'POST' and comment_form.validate():
        if request.method == 'POST':
            print("testestdf")
        print(comment_form.comment.data, datetime.now(), "fdsfdafs")
        new_comment = Comment(body=comment_form.comment.data, timestamp=datetime.now(), user_to_id=user.id, user_from_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
    
    print("testestst")
    return render_template('userpage.html', user=user, high_score=high_score, game_count=game_count, comments=user_comments, form = comment_form)