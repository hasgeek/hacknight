# -*- coding: utf-8 -*-

# The imports in this file are order-sensitive

from pytz import timezone
from flask import Flask
from flask_lastuser import Lastuser
from flask_lastuser.sqlalchemy import UserManager
from flask_mail import Mail
from flask_assets import Environment, Bundle
from baseframe import baseframe, assets, Version
import coaster.app
from ._version import __version__

# First, make an app and config it

version = Version(__version__)
leaflet_version = Version('0.3.0')
app = Flask(__name__, instance_relative_config=True)
lastuser = Lastuser()
mail = Mail()

# Second, after config, import the models and views

import hacknight.models
from hacknight.models import db
import hacknight.views

# Third, setup baseframe and assets

assets['leaflet.css'][leaflet_version] = 'js/leaflet/leaflet.css'
assets['leaflet.js'][leaflet_version] = 'js/leaflet/leaflet.js'
assets['hacknight.css'][version] = 'css/app.css'
assets['hacknight.js'][version] = 'js/scripts.js'


coaster.app.init_app(app)
baseframe.init_app(app, requires=['baseframe', 'toastr', 'hacknight'], bundle_js=assets.require('leaflet.js'), bundle_css=assets.require('leaflet.css'))
lastuser.init_app(app)
lastuser.init_usermanager(UserManager(hacknight.models.db, hacknight.models.User))
mail.init_app(app)
app.config['tz'] = timezone(app.config['TIMEZONE'])
