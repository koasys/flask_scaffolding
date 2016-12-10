from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, TextField, PasswordField, validators
from wtforms import TextAreaField
from flask_wtf import RecaptchaField


class RegistrationForm(Form):
    
    # Commented out because username is not used. Use email instread.
    #username = TextField('Username', [validators.Length(min=4, max=25)])
    
    # Original design was to use email as your username
    # Currently, this form does not check whether input is email
    email = TextField('Username', 
        [ validators.Length(min=3, max=50), validators.Required(),
        validators.EqualTo('email_confirm', message='Email must match') ])
    email_confirm = TextField('Repeat Username')
    # Name
    firstname = TextField('First Name', [validators.Length(min=1, max=30)])
    middlename = TextField('Middle Name', [validators.Length(min=0, max=30)])
    lastname = TextField('Last Name', [validators.Length(min=1, max=30)])
    
    # Password
    password = PasswordField('New Password', [ validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.length(min=8, max=35)])
    confirm = PasswordField('Repeat Password')

    
    
class LoginForm(Form):
    username = TextField('Type Your username')
    password = PasswordField('Password')
    
    
class ChangePasswordForm(Form):
    old_password = PasswordField('Old password')
    new_password = PasswordField('New password',[validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.length(min=8, max=35)])
    confirm = PasswordField('Repeat new password')    
    
    
