from flask import Blueprint , render_template  ,redirect, url_for
from flask_login import current_user
from .models import Event,Date,Result

views = Blueprint('views' , __name__)


@views.route('/WelcomeScreen')
def welcome():
    return render_template("welcomescreen.html")

#home screen 
@views.route('/' , methods = ['GET','POST'])
def home():
    if not current_user.is_authenticated:
        return  redirect(url_for('views.welcome'))
    
    #get all the events from db
    eventList=Event.query.all() 
    DateList = Date.query.all()
    return render_template("home.html" , user = current_user ,eventList=eventList,DateList=DateList)

@views.route('UserEvents' , methods = ['GET'])
def UserEvents():
    results = list()

    result = Result.query.all()

    for r in result:
        if r.user_id == current_user.id:
            results.append(r.result)

    return  render_template("UserEvents.html" , user = current_user , results = results)