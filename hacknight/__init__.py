# -*- coding: utf-8 -*-

# The imports in this file are order-sensitive

from pytz import timezone
from flask import Flask
from flask.ext.lastuser import Lastuser
from flask.ext.lastuser.sqlalchemy import UserManager
from flask.ext.mail import Mail
from flask.ext.assets import Environment, Bundle
from baseframe import baseframe, baseframe_js, baseframe_css
import coaster.app

# First, make an app and config it

app = Flask(__name__, instance_relative_config=True)
lastuser = Lastuser()
mail = Mail()

# Second, after config, import the models and views

import hacknight.models
from hacknight.models import db
import hacknight.views

# Third, setup baseframe and assets

app.register_blueprint(baseframe)

assets = Environment(app)
js = Bundle(baseframe_js,
    'js/leaflet/leaflet.js',
    'js/scripts.js')

css = Bundle(baseframe_css,
    'js/leaflet/leaflet.css',
    'css/app.css')
assets.register('js_all', js)
assets.register('css_all', css)


def init_for(env):
    coaster.app.init_app(app, env)
    lastuser.init_app(app)
    lastuser.init_usermanager(UserManager(hacknight.models.db, hacknight.models.User))
    mail.init_app(app)
    app.config['tz'] = timezone(app.config['TIMEZONE'])
