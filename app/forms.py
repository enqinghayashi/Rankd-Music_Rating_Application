from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Confirm')

class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Change Email')

class EditProfileForm(FlaskForm):
    profile_picture = FileField('Upload New Profile Picture', validators=[Optional()])
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    bio = TextAreaField('Bio', validators=[DataRequired(), Length(max=256)])
    submit = SubmitField('Save Changes')

class FriendForm(FlaskForm):
    searching_friends = StringField('Search by username or name')
    search_friend_id = StringField("Enter friend's User ID")
    submit_search = SubmitField('Search')
    submit_add = SubmitField('Add')