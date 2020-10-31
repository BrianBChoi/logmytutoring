from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm,\
    NewSessionForm
from app.models import User, Session


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/new-session', methods=['GET', 'POST'])
@login_required
def new_session():
    form = NewSessionForm()
    if form.cancel.data:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        session = Session(date=form.date.data, hours=form.hours.data,
                          revenue=form.revenue.data, notes=form.notes.data,
                          tutor=current_user)
        db.session.add(session)
        db.session.commit()
        flash('Your session has been saved!')
        return redirect(url_for('index'))
    return render_template('new_session.html', title='New Session', form=form)


@app.route('/students')
@login_required
def students():
    return render_template('students.html', title='Students')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile')


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.email)
    if form.cancel.data:
        return redirect(url_for('profile'))
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved!')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)


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

        # @login_required will redirect user to login page but not before adding
        # the url of the page they were redirected from to the url of the login
        # page.

        next_page = request.args.get('next')

        # The second conditional ensures that the url following 'next' is a
        # relative path to another page in the website, not some other website

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
