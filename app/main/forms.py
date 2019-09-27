from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed,FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user


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
    image_file = FileField('Snap',validators = [FileRequired(), FileAllowed(['jpg','png'])])
    caption = TextAreaField('Caption',validators=[DataRequired(),Length(min=2,max=150)])
    submit = SubmitField('Post')

class SearchForm(FlaskForm):
    q = StringField(('Search'),validators=[DataRequired()])
    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class CommentForm(FlaskForm):
    body = StringField('Comment',validators=[DataRequired()])
    submit = SubmitField('Submit')