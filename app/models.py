from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
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
    date = db.Column(db.DateTime, index=True)
    hours = db.Column(db.Float)
    revenue = db.Column(db.Float, index=True)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return '<Session {}: {}>'.format(self.date, self.notes)
