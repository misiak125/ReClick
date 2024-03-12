from flask import Flask

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='gordojestpiekny'

    from .auth import auth
    from .views import views

    app.register_blueprint(vievs, url_prefx='/')
    app.register_blueprint(auth, url_prefix='/')

    return app 