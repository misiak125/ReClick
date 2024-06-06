from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from .models import User
from werkzeug.security import check_password_hash
from . import db
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from .forms import LoginForm, RegisterForm, ProfilePictureForm
from .utils.token import confirm_token, generate_token
from .utils.decorators import logout_required
from datetime import datetime
from .utils.functions import flash_errors
from .utils.mail import send_confirm_email
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os


auth=Blueprint('auth', __name__)

login_manager = LoginManager()



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
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)

        return redirect(url_for('views.userpage', userid=user.id))

    flash_errors(form)
    return render_template('login.html', form=form)



@auth.route('/signup', methods=['GET', 'POST'])
@logout_required
def signup():
    form = RegisterForm(request.form)
    profile_picture_form = ProfilePictureForm()

    if request.method == 'POST' and form.validate() and profile_picture_form.validate_on_submit():
        email=form.email.data
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists', 'error')
            return redirect(url_for('auth.signup'))
        if len(form.username.data) > 15:
            flash('Username cannot be longer than 15 characters', 'error')
            return redirect(url_for('auth.signup'))
        
        picture_file = profile_picture_form.profile_picture.data

        if picture_file:
            filename = secure_filename(picture_file.filename)
            filepath = os.path.join(current_app.root_path, 'static/profile_pics', filename)
            picture_file.save(filepath)
        else:
            filename = "default_pfp.jpg"

        new_user = User(form.email.data, form.username.data,
                    form.password.data, is_confirmed=True, profile_picture=filename)

        db.session.add(new_user)
        db.session.commit()
        
        #email confirmation
        
        #!!!! zrezygnowalismy z funkcji potwierdzania maila, bo juz drugi raz nam zbanowali konto :(
        #!!!! ale generalnie dziala :))
        '''
        token = generate_token(new_user.email)
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)
        html = render_template("confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_confirm_email(new_user.email, subject, html)
        
        login_user(new_user)

        flash("A confirmation email has been sent via email.", "happy")
        return redirect(url_for("auth.inactive"))
        '''
        
        flash("Thanks for registering!", "happy")
        return redirect(url_for('auth.login'))
        
        
    flash_errors(form)
    flash_errors(profile_picture_form)
    return render_template('signup.html', form=form, pfp_form=profile_picture_form)
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))

'''
@auth.route("/confirm/<token>")
def confirm_email(token):
    if current_user.is_confirmed:
        flash("Account already confirmed.", "info")
        return redirect(url_for('views.userpage', userid=current_user.id))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.is_confirmed = True
        user.activated_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "happy")
    else:
        flash("The confirmation link is invalid or has expired.", "error")
    return redirect(url_for('views.userpage', userid=user.id))


@auth.route("/inactive")
@login_required
def inactive():
    if current_user.is_confirmed:
        return redirect(url_for('views.userpage', userid=current_user.id))
    return render_template("inactive.html")
    
@auth.route("/resend_confirmation")
@login_required
def resend_confirmation():
    if current_user.is_confirmed:
        flash("Your account has already been confirmed.", "info")
        return redirect(url_for('views.userpage', userid=current_user.id))
    token = generate_token(current_user.email)
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)
    html = render_template("confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_confirm_email(current_user.email, subject, html)
    flash("A new confirmation email has been sent.", "happy")
    return redirect(url_for("auth.inactive"))

'''