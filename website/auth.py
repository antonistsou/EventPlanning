from flask import Blueprint , render_template ,request , flash ,redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash , check_password_hash
from . import db
from flask_login import login_user , login_required , logout_user , current_user

auth = Blueprint('auth' , __name__)

@auth.route('/login' , methods = ['GET' , 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user= User.query.filter_by(email=email).first()
        
        if user : 
            if check_password_hash(user.password , password):
                flash('Logged in !' , category= 'success')
                login_user(user, remember=True)
            else: 
                flash('Incorrect email or password , please try again.' , category='notification')
        else: 
            flash('Account does not exist.')  
    return render_template("login.html" , user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup' , methods = ['GET' , 'POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2') 

        user= User.query.filter_by(email=email).first()
        if user: 
            flash('Account already exists. ', category= 'notification')
        elif len(email) < 4: 
            flash('Email less than 4 characters.' , category='notification')
        elif len(firstName) <1:
            flash('first name is null.' , category='notification')
        elif password1 != password2:
            flash('Passwords don\'t match.' , category='notification')
        elif len(password1)<7:
            flash('Password must be at least 8 characters' , category='notification')
        else: 
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category  = 'success')
            return redirect(url_for('views.home'))

    return render_template("singup.html" , user = current_user)
