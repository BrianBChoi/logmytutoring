from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    sessions = [
        {
            'student': {'name': 'Mate'},
            'notes': 'He did well today!'
        },
        {
            'student': {'name': 'Shreya'},
            'notes': 'We worked on graphing functions today'
        }
    ]
    return render_template('index.html', title='Home', user=user, sessions=sessions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Is the user already logged in? Then redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # This block runs when the user has clicked submit
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # If the user does not exist or the password does not match
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # If login is successful, Flask-Login keeps track of user
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
