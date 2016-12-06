# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort
from flask import render_template, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

from account.views import account_views
from facade.views import facade_views


db = SQLAlchemy()


def create_app():
    # create our little application :)
    app = Flask(__name__)

    
    ### Configure app
    #
    app.config.from_object(__name__)
    # Load default config and override config from an environment variable
    app.config.update(dict(
        #DATABASE=os.path.join(app.root_path, 'tracking_monitoring.db'),
        SECRET_KEY='B1Xp83k/4qY1S~GIH!jnM]KES/,?CT',
        USERNAME='admin',
        PASSWORD='Nimd@'
    ))
    app.config.from_envvar('TRACKERAPP_SETTINGS', silent=True)
    #app.config['db'] = connect_db()

    
    ### Database related
    #
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql+psycopg2://pdbuser:pdbuser@localhost:5432/tracker_monitoring'
        
    db.init_app(app)
    print 'before creating tables...'
    with app.test_request_context():
        print 'creating tables...'
        from account.models import User
        from account.models import UserAccount
        
        db.create_all()
        
        # Create a test user for testing
        auser = User.create(username='tester1', password='tester', 
            firstname='tester', middlename='', lastname='tester', email='t@email.com')
        if auser:
            # If this user is being registered for the first time.
            auser.save()
            
    ### Blueprint setup
    #
    app.register_blueprint(account_views, url_prefix='/account')
    app.register_blueprint(facade_views, url_prefix='')    
    
    # Flask-Login Configuration
    login_manager = LoginManager()
    login_manager.session_protection = "strong"
    login_manager.init_app(app)
    login_manager.login_view = '/account/login'
    
    # Required method to connect Flask-Login with custom User class
    @login_manager.user_loader
    def load_user(username):
        print 'load_user - userid', username
        return User.get_with_username(username)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)
