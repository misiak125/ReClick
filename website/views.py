from flask import Blueprint, render_template, request, abort, jsonify
from flask_login import login_required, current_user
from .models import User, Game
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
@active_login_required
def play():
    return render_template('game.html')

@views.route("/user/<int:userid>", methods=['GET', 'POST'])
@active_login_required
def userpage(userid):
    user = User.query.get(userid)

    game_count = Game.query.filter_by(user_id=userid).count()

    highest_score = Game.query.filter_by(user_id=userid).order_by(Game.score.desc()).first()
    high_score = highest_score.score if highest_score else 0

    if user is None or not user.is_confirmed:
        abort(404)
        
    user_comments = Comment.query.filter_by(user_to_id=user.id)
    comment_form = CommentForm()
   
    if request.method == 'POST' and comment_form.validate():
        print(comment_form.comment.data, datetime.now(), user.id, current_user.id)
        new_comment = Comment(body=comment_form.comment.data, timestamp=datetime.now(), 
                user_to_id=user.id, user_from_id=current_user.id, user_from_name=current_user.name)
        print(new_comment)
        db.session.add(new_comment)
        db.session.commit()
    
    print("testestst")
    return render_template('userpage.html', user=user, high_score=high_score, game_count=game_count, comments=user_comments, form = comment_form)


AUTH_TOKEN = "gordini_wysyla_wynik"
@views.route('/receive_score', methods=['POST'])
@active_login_required

def receive_score():
    try:
        auth_token = request.headers.get('Authorization')
        if auth_token != AUTH_TOKEN:
            abort(401)

        score = request.form.get('score')
        userid = current_user.id 

        new_game = Game(user_id=int(userid), score=int(score))
        db.session.add(new_game)
        db.session.commit()

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

