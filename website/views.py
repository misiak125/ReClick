from flask import Blueprint

views=Blueprint('vievs', __name__)

@views.route('/')
def index():
    return "<p>niga</p>"