from flask import Blueprint , render_template ,request , flash ,redirect, url_for
from flask_login import  login_required , current_user


views = Blueprint('views' , __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html" , user = current_user)


@views.route('/result' , methods = ['GET' , 'POST'])
def result():
    return render_template("result.html" , user = current_user)