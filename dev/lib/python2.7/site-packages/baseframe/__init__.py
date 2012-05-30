# -*- coding: utf-8 -*-

import os
from flask import Blueprint, send_from_directory, render_template
from flask.ext.assets import Bundle

__all__ = ['baseframe', 'baseframe_js', 'baseframe_css']

baseframe = Blueprint('baseframe', __name__,
                      static_folder='static',
                      static_url_path='/baseframe',
                      template_folder='templates')

jquery_js = Bundle('baseframe/js/jquery-1.7.1.js',
                   'baseframe/js/jquery.form.js',
                   'baseframe/js/tiny_mce/jquery.tinymce.js',
                   'baseframe/js/bootstrap-datepicker.js',
                   'baseframe/js/chosen.jquery.js',
                   filters='jsmin', output='js/baseframe-jquery.min.js')


#bootstrap_js = Bundle('baseframe/js/bootstrap/bootstrap-alert.js',
#                      'baseframe/js/bootstrap/bootstrap-button.js',
#                      'baseframe/js/bootstrap/bootstrap-carousel.js',
#                      'baseframe/js/bootstrap/bootstrap-collapse.js',
#                      'baseframe/js/bootstrap/bootstrap-dropdown.js',
#                      'baseframe/js/bootstrap/bootstrap-modal.js',
#                      'baseframe/js/bootstrap/bootstrap-tooltip.js',
#                      'baseframe/js/bootstrap/bootstrap-popover.js',
#                      'baseframe/js/bootstrap/bootstrap-scrollspy.js',
#                      'baseframe/js/bootstrap/bootstrap-tab.js',
#                      'baseframe/js/bootstrap/bootstrap-transition.js',
#                      'baseframe/js/bootstrap/bootstrap-typeahead.js',
#                      filters='jsmin', output='js/baseframe-bootstrap.min.js')

networkbar_js = Bundle('baseframe/js/networkbar.js')
baseframe_js = Bundle(jquery_js,
                      'baseframe/js/bootstrap/bootstrap.min.js',
                      networkbar_js,
                      'baseframe/js/baseframe.js',
                      filters='jsmin', output='js/baseframe-packed.js')


#bootstrap_less = Bundle('baseframe/less/bootstrap/bootstrap.less',
#                        'baseframe/less/bootstrap/responsive.less',
#                        filters='less', output='baseframe/css/bootstrap.css',
#                        debug=False)

networkbar_css = Bundle('baseframe/css/networkbar.css')
baseframe_css = Bundle(  # bootstrap_less,
                       'baseframe/css/bootstrap.css',   # Externally compiled with Less
                       'baseframe/css/responsive.css',  # Externally compiled with Less
                       'baseframe/css/chosen.css',      # Companion to chosen.jquery.js
                       'baseframe/css/baseframe.css',   # Externally compiled with Compass
                       networkbar_css,                  # Externally compiled with Compass
                       filters='cssmin',
                       output='css/baseframe-packed.css')


@baseframe.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(baseframe.root_path, 'static', 'img'),
      'favicon.ico', mimetype='image/vnd.microsoft.icon')


@baseframe.route('/humans.txt')
def humans():
    return send_from_directory(os.path.join(baseframe.root_path, 'static'),
                               'humans.txt', mimetype='text/plain')


@baseframe.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(baseframe.root_path, 'static'),
                               'robots.txt', mimetype='text/plain')


@baseframe.app_errorhandler(404)
def error404(e):
    return render_template('404.html'), 404


@baseframe.app_errorhandler(403)
def error403(e):
    return render_template('403.html'), 403


@baseframe.app_errorhandler(500)
def error500(e):
    return render_template('500.html'), 500
