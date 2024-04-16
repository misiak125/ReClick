from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import manage.py

db = SQLAlchemy()
DB_NAME="database.db"


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='gordojestpiekny'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)


    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefx='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()

    app.cli.add_command(manage.create_admin)

    return app 


