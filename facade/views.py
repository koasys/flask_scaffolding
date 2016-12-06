from flask import render_template, Blueprint
from flask import Flask, current_app, session
from flask.ext.login import login_user, login_required



# Define the blueprint
facade_views = Blueprint('facade', __name__, template_folder='templates',
    static_folder='static')
    

@facade_views.route('/')
def index():
    debug_set = current_app.config["DEBUG"]   # settings.DEBUG
    if debug_set == True :
        print "\n\n\n==========> facade->views.py -> index() "
    return render_template('index.html')  


#@facade_views.route('/initiate_tracker_db')
#def initiate_tracker_db():
#    with current_app.app_context():
#        db.create_all()

@facade_views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')  
