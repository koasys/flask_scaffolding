from flask_wtf import FlaskForm as Form
#import FlaskForm as Form
from wtforms import BooleanField, TextField, PasswordField, validators
from wtforms import TextAreaField
from flask_wtf import RecaptchaField


class RegistrationForm(Form):
    #username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email &nbsp;&nbsp; (This email will be your usename.)', 
        [ validators.Length(min=3, max=50), validators.Required(),
        validators.EqualTo('email_confirm', message='Email must match') ])
    email_confirm = TextField('Repeat Email')
    firstname = TextField('First Name', [validators.Length(min=1, max=30)])
    middlename = TextField('Middle Name', [validators.Length(min=0, max=30)])
    lastname = TextField('Last Name', [validators.Length(min=1, max=30)])
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
    
    
