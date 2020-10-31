from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    IntegerField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    name = StringField('First and Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Flask-WTF automatically uses these methods as validators because of the
    # way they're named (validate_<fieldname>)

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    name = StringField('First and Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

    def __init__(self, default_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.default_email=default_email

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and email.data != self.default_email:
            raise ValidationError('Please use a different email address.')

class NewSessionForm(FlaskForm):
    student = StringField('Student', validators=[DataRequired()])
    date = DateTimeField('Date', validators=[DataRequired()])
    hours = IntegerField('Hours', validators=[DataRequired()])
    revenue = IntegerField('Revenue', validators=[DataRequired()])
    notes = StringField('Notes', validators=[DataRequired()])
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')
