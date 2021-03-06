from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm,\
    NewSessionForm, NewStudentForm, ResetPasswordRequestForm,\
    ResetPasswordForm
from app.models import User, Session, Student
from app.email import send_password_reset_email


@app.route('/')
@app.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    sessions = current_user.new_sessions().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=sessions.next_num) \
        if sessions.has_next else None
    prev_url = url_for('index', page=sessions.prev_num) \
        if sessions.has_prev else None
    return render_template('index.html', title='Home', sessions=sessions.items,
                           next_url=next_url, prev_url=prev_url)


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


@app.route('/new-student', methods=['GET', 'POST'])
@login_required
def new_student():
    form = NewStudentForm()
    if form.cancel.data:
        return redirect(url_for('students'))
    if form.validate_on_submit():
        student = Student(name=form.name.data, hourly_rate=form.hourly_rate.data,
                          tutor=current_user)
        db.session.add(student)
        db.session.commit()
        flash('The student has been added!')
        return redirect(url_for('students'))
    return render_template('new_student.html', title='New Student', form=form)


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



@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
