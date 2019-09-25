from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2,max=20)])
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=15)])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self,email):
        user  = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already registered!")

    def validate_username(self,username):
        user  = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Oops someone already have this username!!")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=15)])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    image_file = FileField('Update Profile picture',validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user  = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Oops someone already have this username!!")


class PostForm(FlaskForm):
    image = FileField('Snap',validators = [DataRequired(),FileAllowed(['jpg','png'])])
    caption = TextAreaField('Caption',validators=[DataRequired(),Length(min=2,max=150)])
    submit = SubmitField('Post')