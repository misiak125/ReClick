from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in.", "info")
            return redirect(url_for("views.profile"))
        return func(*args, **kwargs)

    return decorated_function

def active_login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated is False:
            flash("Please log in to access this page.", "info")
            return redirect(url_for("views.profile"))
        if current_user.is_confirmed is False:
            flash("Please confirm your account", "error")
            return redirect(url_for("auth.inactive"))
        return func(*args, **kwargs)

    return decorated_function