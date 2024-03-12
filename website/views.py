from flask import Blueprint

vievs=Blueprint('vievs', __name__)

@vievs.route('/')
def index():
    return "<p>niga</p>"