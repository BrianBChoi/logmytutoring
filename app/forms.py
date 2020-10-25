from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
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
    name = StringField('First and Last Name', validators=[DataRequired()]
                        default=current_user.name)
    email = StringField('Email', validators=[DataRequired(), Email()]
                        default=current_user.email)
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and email.data is not current_user.email:
            raise ValidationError('Please use a different email address.')
