from flask import render_template, Blueprint
from flask import Flask, current_app, session
from flask_login import login_user, login_required


# Define the blueprint
main_views = Blueprint('main', __name__, template_folder='templates',
    static_folder='static')


@main_views.route('/index')
@login_required
def index():
    return render_template('main_index.html')  




