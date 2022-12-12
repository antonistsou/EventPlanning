from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__) 
    #database key 
    app.config['SECRET_KEY'] = 'fsefgsergsgrgb'
    #database location 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)


    from .views import views
    from .auth import auth

    #blueprints prefix url 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User 

    #db creation
    with app.app_context():
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print('_________________ DB created! ___________________')

    #redirect if login required : login page
    login_manager = LoginManager()
    login_manager.login_view = 'views.welcomescreen'
    login_manager.init_app(app)

    #user load that relates to this id 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
    

