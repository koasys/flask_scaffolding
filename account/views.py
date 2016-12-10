from flask import Blueprint, render_template, abort, request, redirect, flash
from flask import url_for
from jinja2 import TemplateNotFound
from flask import current_app, session
from models import User
from models import NotUniqueException
from forms import RegistrationForm, LoginForm
from forms import ChangePasswordForm
from flask_login import login_user, login_required
from flask_login import logout_user, current_user
from flask_mail import Message, Mail
import utils
from utils import csrf_protect

from werkzeug.security import generate_password_hash
#encryption_method = 'pbkdf2:sha256:5000'

account_views = Blueprint('account', __name__, template_folder='templates',  static_folder='static')

@account_views.route('/hiddensignup', methods=['GET','POST'])
def signup():
    error = None
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User.create(username=form.email.data, email=form.email.data,
            firstname=form.firstname.data, middlename=form.middlename.data, 
            lastname=form.lastname.data, password=form.password.data)
        if user is not None:
            user.save()
            flash('Thanks for registering')
            # TODO: Send a validation email.
            return render_template('signup_done.html')
        else:
            error = 'Your email has been already used! Use new email address.'
        
    return render_template('signup.html', form=form, error=error)
    
    
@account_views.route('/login', methods=['GET','POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        username = form.username.data
        password = form.password.data
        user = User.get_with_username(username)

        if user and user.is_active() and not user.is_anonymous():
            if user.authenticate(password):
                login_user(user)
                flash("Logged in successfully.")
                return redirect(request.args.get("next") or url_for("main.index"))
            else:
                error = "Your username or password is not valid"
                
    return render_template("login.html", form=form, error=error)


@account_views.route('/logout')
@login_required
def logout():
    logout_user() 
    return redirect('/')


@account_views.route('/changepassword', methods=['GET','POST'])
@login_required
def change_password():
    '''
    Change a user's password
    '''
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.update_password(form.new_password.data)
            current_user.save()
            flash("Your password has been updated.", category='index_page')
            return redirect(request.args.get("next") or url_for("main.index"))
        else:
            flash("Your password does not match.", category='error')
            return render_template('change_password.html', form=form)    
    return render_template('change_password.html', form=form)
