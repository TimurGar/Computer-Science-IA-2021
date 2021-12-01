from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from myapp.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Functions that make sure newly registered users don't have same usernames and/or emails.
    # Meaning username and email of each user should be unique
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')


class NewProjectForm(FlaskForm):
    name = StringField('Project name', validators=[DataRequired()])
    description = TextAreaField('Project description', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


class EditProjectForm(FlaskForm):
    name = StringField('Project name', validators=[DataRequired()])
    description = TextAreaField('Project description', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


class NewItemForm(FlaskForm):
    name = StringField('Item name', validators=[DataRequired()])
    description = TextAreaField('Item description', validators=[Length(min=0, max=140)])
    model_or_type = StringField('Model/Type')
    size = StringField('Size (length*width*height)')
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    weight = IntegerField('Weight(g)')
    cost = IntegerField('Cost ($USD)', validators=[DataRequired()])
    submit = SubmitField('Add Item')


class SearchForm(FlaskForm):
    search = StringField()
    submit = SubmitField('Search')