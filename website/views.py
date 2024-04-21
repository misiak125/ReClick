from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from flask_mailman import EmailMessage

views=Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name) #test

@views.route('/testmail')
def testmail():
    msg = EmailMessage(
        'hejhej temat',
        'hejka tresc',
        're.click@outlook.com',
        ['kapi.misiak@gmail.com']
    )
    msg.send()
    return "chyba wyslane"
