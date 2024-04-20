from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from werkzeug.security import check_password_hash
from . import db
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from .forms import LoginForm, RegisterForm
from .token import confirm_token, generate_token
from .utils.decorators import logout_required

auth=Blueprint('auth', __name__)

login_manager = LoginManager()

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'error')


@auth.route('/login', methods=['POST', 'GET'])
@logout_required
def login():

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        remember = form.remember_me.data

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)

        return redirect(url_for('views.profile'))

    flash_errors(form)
    return render_template('login.html', form=form)



@auth.route('/signup', methods=['GET', 'POST'])
@logout_required
def signup():
    form = RegisterForm(request.form)
    
    if request.method == 'POST' and form.validate():
        email=form.email.data
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
            
        new_user = User(form.email.data, form.username.data,
                    form.password.data, is_active=True)
        db.session.add(new_user)
        db.session.commit()
        token = generate_token(user.email)
        flash('Thanks for registering')
        return redirect(url_for('auth.login'))
    flash_errors(form)
    return render_template('signup.html', form=form)
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@auth.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if current_user.is_confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for('views.profile'))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "happy")
    else:
        flash("The confirmation link is invalid or has expired.", "error")
    return redirect(url_for("views.profile"))
