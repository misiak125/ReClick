from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mailman import Mail


db = SQLAlchemy()
DB_NAME="database.db"

def create_app():
    app=Flask(__name__)

    app.config['SECRET_KEY']= 'gordopieknyjest'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    '''
    app.config['MAIL_SERVER'] = "smtp-mail.outlook.com"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = "re.click@outlook.com"
    app.config['MAIL_PASSWORD'] = ""
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['SECURITY_PASSWORD_SALT'] = "devdev"
    '''

    mail=Mail(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)
    login_manager.login_message_category = "info"


    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    

    from .auth import auth
    from .views import views, usersbp

    app.register_blueprint(views, url_prefx='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(usersbp, url_prefix='/user')
    
    with app.app_context():
        db.create_all()

    from .manage import user_cli
    app.register_blueprint(user_cli)
    

    return app 


