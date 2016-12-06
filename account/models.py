import json
import string
import random
from flask.ext.login import UserMixin
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


# Instantiate db from SQLAlchemy
db = SQLAlchemy()

# Configuration Parameters
# ------------------------
#encryption_method = 'pbkdf2:sha256:5000'


# Custom Exception
# 
class NotUniqueException(Exception):
    '''
    If an object to handle is not unique and already exists in a system.
    '''
    def __init__(self, mssg):
        self.mssg = mssg


# Classes
#
class User(UserMixin):
    '''
    User object that will be managed by Flask-Login and work with SQLAlchemy.
    '''
    def __init__(self, username, firstname, middlename, lastname, email, 
            active, anonymous, password_hash=''):
        self.active = active
        self.anonymous = anonymous
        self.username = username
        self.password_hash = password_hash
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
    
    
    def authenticate(self, password):
        # if password is same with password in db
        # set self.authenticated = True
        return check_password_hash(self.password_hash, password)
            
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
        
    def update_password(self, newone):
        self.password_hash = generate_password_hash(newone)    

        
    def save(self):
        # Get db object
        #db = current_app.config["db"]
        # Make UserAccount to update
        obj_json = json.dumps(self, default=lambda o: o.__dict__)
        
        user = UserAccount.query.filter_by(username=self.username).first()
        if user:
            # Update curr user
            UserAccount.query.filter_by(username=self.username).first().update(
                obj_json)
        else:
            # Insert new user
            user = UserAccount(username=self.username, 
                firstname=self.firstname, password=self.password_hash,
                middlename=self.middlename, lastname=self.lastname,
                email=self.email, is_active=self.active, 
                is_anonymous=self.anonymous) 
            db.session.add(user)
            
        db.session.commit()
        
        #mongo = current_app._get_current_object().data.driver
        #obj_str = json.dumps(self, default=lambda o: o.__dict__)
        #obj = json.loads(obj_str)
        #print 'new user json is: %s' % obj_str
        #mongo.db.users.update({'username':self.username},obj, upsert=True)
        
        
    @staticmethod
    def create(username, password, firstname, middlename, lastname, email):
        #db = current_app.config["db"]
        #mongo = current_app._get_current_object().data.driver
        # To check if username is already existing.
        #user = mongo.db.users.find_one({'username': username})
        #user = db.session.query().filter(UserAccount.username=self.username).first()
        user = UserAccount.query.filter_by(username=username).first()
        
        if user:
            print 'current db name"', user.username
            print 'the new user already exists!'
            return None # the username is already existing. Throw an exception.
        else:
            # Generate a salted password by using PBKDF2-SHA256
            password_hash = generate_password_hash(password)
           
            new_user = User(username=username, password_hash=password_hash,
                firstname=firstname, middlename=middlename, lastname=lastname,
                email=email, active=True, anonymous=False)
        
            return new_user       
        
        
    @staticmethod
    def get_with_username(username=''):
        '''
        Return User object that matches a given username by reading a db.
        This method should be called inside of request context in order to get
        current_app object.
        '''
        #mongo = current_app._get_current_object().data.driver
        #db = current_app.config["db"]
        
        #user = mongo.db.users.find_one({'username': username})
        user = UserAccount.query.filter_by(username=username).first()
        
        if user is None:
            return None
        
        return User(username=user.username,  firstname=user.firstname, 
            middlename=user.middlename, lastname=user.lastname, 
            email=user.email, password_hash=user.password, 
            active=user.is_active, anonymous=False)
            
            
    @staticmethod
    def get_with_userid(userid):
        #mongo = current_app._get_current_object().data.driver
        #db = current_app.config["db"]
        #user = mongo.db.users.find_one({'_id': ObjectId(useroid)})
        return UserAccount.query.filter_by(id=userid).first()
        

    # methods for Flask-Login user
    # ===
    def is_authenticated(self):
        ''' Assume all User object after login point are authenticated. 
            That means that if you have User ID stored in user session,
            it is authenticated.
        '''
        return True
        
    def is_active(self):
        return self.active
    
        
    def is_anonymous(self):
        return self.anonymous
    
    
    def get_id(self):
        return self.username       
                  

class UserAccount(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200), unique=False)
    firstname = db.Column(db.String(30), unique=False)
    middlename = db.Column(db.String(30), unique=False)
    lastname = db.Column(db.String(30), unique=False)
    email = db.Column(db.String(50), unique=True)
    is_active = db.Column(db.Boolean())
    is_anonymous = db.Column(db.Boolean())

                               
    def __init__(self, username, password, firstname,middlename,lastname,email,
            is_active,is_anonymous):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
        self.is_active = is_active
        self.is_anonymous = is_anonymous
        

    def __repr__(self):
        return '<UserAccount %r>' % self.username

    