from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=12)])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm password', validators=[EqualTo('password')])
    submit = SubmitField('Register!')

class LoginForm(FlaskForm):
    
    username_or_email = StringField('Email or username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in!')