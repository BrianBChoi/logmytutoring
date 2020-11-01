from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


# Tells flask-login the info in the database about the specified user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    students = db.relationship('Student', backref='tutor', lazy='dynamic')
    sessions = db.relationship('Session', backref='tutor', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def new_sessions(self):
        return self.sessions.order_by(Session.date.desc())

    def new_students(self):
        return self.students.order_by(Student.id.desc())

    def revenue_this_month(self):
        revenue = 0
        for session in self.sessions.all():
            if session.revenue is not None:
                if session.date.month == datetime.now().month:
                    revenue += session.revenue
        return "{:n}".format(revenue)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    hourly_rate = db.Column(db.Float, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    sessions = db.relationship('Session', backref='student', lazy='dynamic')

    def __repr__(self):
        return '<Student {}>'.format(self.name)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    hours = db.Column(db.Float)
    revenue = db.Column(db.Float, index=True)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return '<Session {}: {}>'.format(self.date, self.notes)
