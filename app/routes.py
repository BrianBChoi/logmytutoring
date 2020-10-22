from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
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
    form = LoginForm()
    if form.validate_on_submit():
        # Temporary flash message until we set up database
        flash('Login requested for user {}, remember_me={}'.format
            (form.username.data, form.remember_me.data))
        return redirect(url_for('/index'))
    return render_template('login.html', title='Sign In', form=form)
