from flask import url_for
from flask_wtf import  FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from App.User import User

class SignUpWithEmailAndPassword(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired(message="Don't you have a name? (This field cannot be blank!)"), Length(min=5, message="That's not your real name, is it? (This field must contain at least 5 characters!)")])
    email = StringField(label="Email address", validators=[DataRequired(message="Please enter your email address (This field cannot be blank!)"), Email(message="This doesn't look right!")])
    password = StringField(label="Password", validators=[DataRequired(message="A password-less account? Thats new! (This field cannot be blank!)"), Length(min=8, message="Please give a more secure password!")])
    password2 = StringField(label="Repeat password", validators=[DataRequired("Do you remember your password? (This field cannot be blank!)"), EqualTo('password', message="Are you sure that the two passwords match?")])
    submit = SubmitField(label="Sign Up")

    def validate_email(self, email):
        user = User()
        user.getUserByEmail(email.data)

        if  user.isUser():
            print('err')
            raise ValidationError(message="There is already a user with this email. Please <a href='" + url_for('signin') + "'>login</a>")

class SignInWithEmailAndPassword(FlaskForm):
    email = StringField(label="Email address", validators=[DataRequired(message="Please enter your email address (This field cannot be blank!)"), Email(message="This doesn't look right!")])
    password = StringField(label="Password", validators=[DataRequired(message="A password-less account? Thats new! (This field cannot be blank!)")])
    submit = SubmitField(label="Sign In")

    def validate_email(self, email):
        user = User()
        user.getUserByEmail(email.data)

        if not user.isUser():
            raise ValidationError(message="There is no user with this email. Please <a href='" + url_for('signup') + "'>sign up</a>")
        elif user.provider != "password":
            raise ValidationError(message=f'Please sign in with {user.provider}')

class ForgotPassword(FlaskForm):
    email = StringField(label="Email address", validators=[DataRequired(message="Please enter your email address (This field cannot be blank!)"), Email(message="This doesn't look right!")])
    submit = SubmitField(label="Submit")

    def validate_email(self, email):
        user = User()
        user.getUserByEmail(email.data)

        if not user.isUser():
            raise ValidationError(
                message="There is no user with this email. Please <a href='" + url_for('signup') + "'>sign up</a>")
        elif user.provider != "password":
            raise ValidationError(message=f'Please sign in with {user.provider}')

class ResetPassword(FlaskForm):
    email = StringField(label="Email address")
    password = StringField(label="Password", validators=[DataRequired(message="A password-less account? Thats new! (This field cannot be blank!)"), Length(min=8, message="Please give a more secure password!")])
    password2 = StringField(label="Repeat password", validators=[DataRequired("Do you remember your password? (This field cannot be blank!)"), EqualTo('password', message="Are you sure that the two passwords match?")])
    submit = SubmitField(label="Change Password")

class ChangePassword(FlaskForm):
    current_password = StringField(label='Current Password', validators=[DataRequired(message="A password-less account? Thats new! (This field cannot be blank!)"), Length(min=8, message="Please give a more secure password!")])
    password = StringField(label="New Password", validators=[DataRequired(message="A password-less account? Thats new! (This field cannot be blank!)"),Length(min=8, message="Please give a more secure password!")])
    password2 = StringField(label="Repeat New password",validators=[DataRequired("Do you remember your password? (This field cannot be blank!)"),EqualTo('password', message="Are you sure that the two passwords match?")])
    submit = SubmitField(label="Change Password")

class DeleteAccount(FlaskForm):
    current_password = StringField(label='Current Password', validators=[DataRequired(message="A password-less account? Thats new! (This field cannot be blank!)"),Length(min=8, message="Please give a more secure password!")])
    submit = SubmitField(label="Delete Account")

class DashboardName(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired(message="Don't you have a name? (This field cannot be blank!)"), Length(min=5, message="That's not your real name, is it? (This field must contain at least 5 characters!)")])
    submit = SubmitField(label="Save")

class DashboardEmail(FlaskForm):
    email = StringField(label="Email address", validators=[DataRequired(message="Please enter your email address (This field cannot be blank!)"), Email(message="This doesn't look right!")])
    submit = SubmitField(label="Save")

    def validate_email(self, email):
        user = User()
        user.getUserByEmail(email.data)

        if user.isUser():
            raise ValidationError(message="There is already a user with this email.")

class MFACode(FlaskForm):
    MFACode = StringField(label="MFA Code", validators=[DataRequired(message="This field cannot be blank!"), Length(min=6, max=6, message="This field must contain 6 numbers")])
    submit = SubmitField(label="Confirm MFA Code")

class AdminEdit(FlaskForm):
    user = StringField()
    item = StringField()
    value = StringField(DataRequired(message="This field cannot be blank!"))
    submit = SubmitField()

class AdminChange(FlaskForm):
    user = StringField()
    item = StringField()
    submit = SubmitField()