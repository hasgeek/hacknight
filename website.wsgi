import sys
import os.path
sys.path.insert(0, os.path.dirname(__file__))
from hacknight import app as application, init_for
init_for('production')