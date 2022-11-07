from flask import Blueprint , render_template ,request , flash

auth = Blueprint('auth' , __name__)

@auth.route('/login' , methods = ['GET' , 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/signup' , methods = ['GET' , 'POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2') 

        if len(email) < 4: 
            flash('Email less than 4 characters.' , category='notification')
        elif len(firstName) <1:
            flash('first name is null.' , category='notification')
        elif password1 != password2:
            flash('Passwords don\'t match.' , category='notification')
        elif len(password1)<7:
            flash('Password must be at least 8 characters' , category='notification')
        else: 
            flash('Account created!', category  = 'success')

    return render_template("singup.html")
