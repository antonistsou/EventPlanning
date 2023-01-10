from flask import Blueprint , render_template ,request , flash ,redirect, url_for
from flask_login import  login_required , current_user
import  website.WebScraper
from .models import Event,Date

views = Blueprint('views' , __name__)


@views.route('/WelcomeScreen')
def welcome():
    return render_template("welcomescreen.html")

#home screen 
@views.route('/' , methods = ['GET','POST'])
def home():
    if not current_user.is_authenticated:
        return  redirect(url_for('views.welcome'))
    #data scraper used
    # website.WebScraper.get_Thess_Guide_events()
    #get all the events from db
    eventList=Event.query.all() 
    DateList = Date.query.all()
    return render_template("home.html" , user = current_user ,eventList=eventList,DateList=DateList)

@views.route('UserEvents' , methods = ['GET'])
def UserEvents():
    return render_template("UserEvents.html" , user = current_user)

