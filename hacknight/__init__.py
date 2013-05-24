# -*- coding: utf-8 -*-

# The imports in this file are order-sensitive

from pytz import timezone
from flask import Flask
from flask.ext.lastuser import Lastuser
from flask.ext.lastuser.sqlalchemy import UserManager
from flask.ext.mail import Mail
from flask.ext.assets import Environment, Bundle
from baseframe import baseframe, assets, Version
import coaster.app
from ._version import __version__

# First, make an app and config it

version = Version(__version__)
app = Flask(__name__, instance_relative_config=True)
lastuser = Lastuser()
mail = Mail()

# Second, after config, import the models and views

import hacknight.models
from hacknight.models import db
import hacknight.views

# Third, setup baseframe and assets

app.register_blueprint(baseframe)
assets['leaflet.css'][version] = 'js/leaflet/leaflet.css'
assets['leaflet.js'][version] = 'js/leaflet/leaflet.js'
assets['hacknight.css'][version] = 'css/app.css'
assets['hacknight.js'][version] = 'js/scripts.js'


def init_for(env):
    coaster.app.init_app(app, env)
    baseframe.init_app(app, requires=['baseframe', 'hacknight', 'leaflet'])
    lastuser.init_app(app)
    lastuser.init_usermanager(UserManager(hacknight.models.db, hacknight.models.User))
    mail.init_app(app)
    app.config['tz'] = timezone(app.config['TIMEZONE'])
