# IMPORTS
from flask import Blueprint, render_template, flash, redirect, url_for, session
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app import db
from models import User
from users.forms import RegisterForm, LoginForm
from datetime import datetime
import pyotp

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        pin_key=form.pin_key.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # sends user to login page
        return redirect(url_for('users.login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # If statement to create attribute logins if not already created
    if session.get('logins'):
        session['logins'] = 0

    # Password attempt capped at 3 times and error message presented
    elif session.get('logins') >= 3:
        flash('Limit of password attempts ')

    form = LoginForm()
    # Checking the form is valid
    if form.validate_on_submit():

        # Login try's are added by one
        session['logins'] += 1

        user = User.query.filter_by(email=form.email.data).first()
        # If this is returned then the user is already stored in the database

        # If no user is found then users will be asked to try again
        if not user or not check_password_hash(user.password, form.password.data):
            flash('Please make sure you login details are correct and try again.')

            return render_template('login.html', form=form)

        # Checking if the users pin key and time based pin match
        if pyotp.TOTP(user.pin_key).verify(form.pin.data):

            # if the user is logged in then the number of attempts is reset
            session['logins'] = 0

            login_user(user)

            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            db.session.add(user)
            db.session.commit()

        else:
            flash("Your 2FA is wrong!")

        return login()
    return render_template('login.html', form=form)


# view user logout
@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# view user profile
@users_blueprint.route('/profile')
def profile():
    return render_template('profile.html', name="PLACEHOLDER FOR FIRSTNAME")


# view user account
@users_blueprint.route('/account')
def account():
    return render_template('account.html',
                           acc_no="PLACEHOLDER FOR USER ID",
                           email="PLACEHOLDER FOR USER EMAIL",
                           firstname="PLACEHOLDER FOR USER FIRSTNAME",
                           lastname="PLACEHOLDER FOR USER LASTNAME",
                           phone="PLACEHOLDER FOR USER PHONE")
