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
    'js/scripts.js', 'js/leaflet/leaflet.js',
    )

css = Bundle(baseframe_css,
             'css/app.css', 'js/leaflet/leaflet.css',)
assets.register('js_all', js)
assets.register('css_all', css)

# Fourth, setup admin for the models

#from flask.ext import admin
#from flask.ext.admin.datastore.sqlalchemy import SQLAlchemyDatastore
#from hacknight.views.login import lastuser

#admin_datastore = SQLAlchemyDatastore(hacknight.models, hacknight.models.db.session)
#admin_blueprint = admin.create_admin_blueprint(admin_datastore,
#    view_decorator=lastuser.requires_permission('siteadmin'))

#app.register_blueprint(admin_blueprint, url_prefix='/admin')
