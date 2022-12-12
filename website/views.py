from flask import Blueprint , render_template ,request , flash ,redirect, url_for
from flask_login import  login_required , current_user
import  website.WebScraper

views = Blueprint('views' , __name__)

#home screen 
@views.route('/' , methods = ['GET'])
def home():
    
    if not current_user.is_authenticated:
        return  redirect(url_for('views.welcome'))
    #get all the events
    eventList= website.WebScraper.get_Thess_Guide_events()
    return render_template("home.html" , user = current_user  ,eventList = eventList)


@views.route('/result' , methods = ['GET' , 'POST'])
def result():
    return 0
    # import requests

    # htmlsourceCode = getVivaSourceCode()
    # soup = BeautifulSoup(htmlsourceCode , 'html.parser')
   
    # return htmlsourceCode
    # # return  render_template("result.html" , user = current_user, eventList = eventList)

@views.route('/WelcomeScreen')
def welcome():
    return render_template("welcomescreen.html")