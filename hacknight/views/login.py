# -*- coding: utf-8 -*-

from flask import Response, redirect, flash, g
from flask_lastuser import LastUser
from flask_lastuser.sqlalchemy import UserManager
from coaster.views import get_next_url

from hacknight import app, lastuser
from hacknight.models import db, User, Profile, PROFILE_TYPE


@app.route('/login')
@lastuser.login_handler
def login():
    return {'scope': 'id email organizations'}


@app.route('/logout')
@lastuser.logout_handler
def logout():
    flash("You are now logged out", category='info')
    return get_next_url()


@app.route('/login/redirect')
@lastuser.auth_handler
def lastuserauth():
    Profile.update_from_user(g.user, db.session, type_user=PROFILE_TYPE.PERSON, type_org=PROFILE_TYPE.ORGANIZATION)
    db.session.commit()
    return redirect(get_next_url())


@app.route('/login/notify', methods=['POST'])
@lastuser.notification_handler
def lastusernotify(user):
    Profile.update_from_user(user, db.session, type_user=PROFILE_TYPE.PERSON, type_org=PROFILE_TYPE.ORGANIZATION)
    db.session.commit()


@lastuser.auth_error_handler
def lastuser_error(error, error_description=None, error_uri=None):
    if error == 'access_denied':
        flash("You denied the request to login", category='error')
        return redirect(get_next_url())
    return Response("Error: %s\n"
                    "Description: %s\n"
                    "URI: %s" % (error, error_description, error_uri),
                    mimetype="text/plain")
