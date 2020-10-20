from flask import render_template
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

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
