from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_apscheduler import APScheduler

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__) 
def create_app():
    
    #database key 
    app.config['SECRET_KEY'] = 'fsefgsergsgrgb'
    #database location 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .result import res
    
    #blueprints prefix url 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(res, url_prefix='/')


    from .models import User 
 
    #db creation
    with app.app_context():
           
        if not path.exists('instance/' + DB_NAME):
            db.create_all()
            print('_________________ DB created! ___________________')
        else:
            print("----------------------------------Connection Establisted-----------------------------------------")   
    # with app.app_context():
    #     import website.WebScraper
    #     website.WebScraper.get_Thess_Guide_events()
    # scheduler = APScheduler()
    # scheduler.add_job(id ='Scheduled task', func = DataUpdate, trigger = 'interval', hours  = 24)
    # scheduler.start()

    #redirect if login required : login page
    login_manager = LoginManager()
    login_manager.login_view = 'views.welcomescreen'
    login_manager.init_app(app)

    #user load that relates to this id 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
    

def DataUpdate():
    with app.app_context():
        import website.WebScraper
        website.WebScraper.get_Thess_Guide_events()