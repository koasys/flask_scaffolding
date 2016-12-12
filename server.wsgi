## For virtualenv
#
#activate_this = '/home/gtadmin/PYENV/ENV_gtserver/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

# put server.py into python path.
import sys, os

curr_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, curr_folder)

from server import app as application
