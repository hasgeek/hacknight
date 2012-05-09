import sys
import os.path
from os import environ
sys.path.insert(0, os.path.dirname(__file__))
environ['ENVIRONMENT'] = 'prod'
from hacknight import app as application
