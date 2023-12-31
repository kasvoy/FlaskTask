from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, Optional
from .models import User, db

class RegistrationForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm password', validators=[EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if db.session.scalars(db.Select(User).where(User.username == username.data)).first():
            raise ValidationError(f'{username.data} is already taken')

    def validate_email(self, email):
        if db.session.scalars(db.Select(User).where(User.email == email.data)).first():
            raise ValidationError("A user with this email already exists.")


class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    create = SubmitField('Submit')

class TaskForm(FlaskForm):
    todo= TextAreaField('To do', validators=[DataRequired()])
    due_by = DateField('Due by', validators=[Optional()])
    create = SubmitField('Submit')