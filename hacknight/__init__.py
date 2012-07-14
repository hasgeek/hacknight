# -*- coding: utf-8 -*-

# The imports in this file are order-sensitive

from flask import Flask
from flask.ext.assets import Environment, Bundle
from baseframe import baseframe, baseframe_js, baseframe_css
from coaster import configureapp

# First, make an app and config it

app = Flask(__name__, instance_relative_config=True)
configureapp(app, 'ENVIRONMENT')

# Second, after config, import the models and views

import hacknight.models
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
