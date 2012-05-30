# -*- coding: utf-8 -*-
"""
    flaskext.lastuser.sqlalchemy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    SQLAlchemy extensions for flask-lastuser.

    :copyright: (c) 2011-12 by HasGeek Media LLP.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

__all__ = ['UserBase', 'UserManager']

import urlparse
from flask import g, current_app, json, session
from sqlalchemy import func, Column, Integer, String, DateTime, Unicode, UnicodeText
from sqlalchemy.orm import deferred, undefer
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.lastuser import UserInfo


class UserBase(object):
    """
    Base class for user definition.
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    userid = Column(String(22), unique=True, nullable=False)
    username = Column(Unicode(80), unique=True, nullable=True)  # Usernames are optional
    fullname = Column(Unicode(80), default=u'', nullable=False)
    email = Column(Unicode(80), unique=True, nullable=True)  # We may not get an email address
    # Access token info
    lastuser_token = Column(String(22), nullable=True, unique=True)
    lastuser_token_type = Column(Unicode(250), nullable=True)
    lastuser_token_scope = Column(Unicode(250), nullable=True)

    # Userinfo
    @declared_attr
    def _userinfo(cls):
        return deferred(Column('userinfo', UnicodeText, nullable=True))

    @property
    def userinfo(self):
        if not hasattr(self, '_userinfo_cached'):
            if not self._userinfo:
                self._userinfo_cached = {}
            else:
                self._userinfo_cached = json.loads(self._userinfo)
        return self._userinfo_cached

    @userinfo.setter
    def userinfo(self, value):
        if not isinstance(value, dict):
            raise ValueError("userinfo must be a dict")
        self._userinfo_cached = value
        self._userinfo = json.dumps(value)

    def __repr__(self):
        return '<User %s (%s) "%s">' % (self.userid, self.username, self.fullname)

    def organizations_owned(self):
        if self.userinfo.get('organizations') and 'owner' in self.userinfo['organizations']:
            return list(self.userinfo['organizations']['owner'])
        else:
            return []

    def organizations_owned_ids(self):
        return [org['userid'] for org in self.organizations_owned()]

    def user_organization_ids(self):
        return [self.userid] + self.organizations_owned_ids()

    @property
    def profile_url(self):
        return urlparse.urljoin(current_app.config['LASTUSER_SERVER'], 'profile')


class UserManager(object):
    """
    User manager that automatically loads the current user's object from the database.
    """
    def __init__(self, db, usermodel):
        self.db = db
        self.usermodel = usermodel

    def before_request(self):
        if session.get('lastuser_userid'):
            # TODO: How do we cache this? Connect to a cache manager
            user = self.usermodel.query.filter_by(userid=session['lastuser_userid']
                ).options(undefer('_userinfo')).first()
            if user is None:
                user = self.usermodel(userid=session['lastuser_userid'])
                self.db.session.add(user)
            g.user = user
            g.lastuserinfo = UserInfo(userid=user.userid,
                                      username=user.username,
                                      fullname=user.fullname,
                                      email=user.email,
                                      permissions=user.userinfo.get('permissions', ()),
                                      organizations=user.userinfo.get('organizations'))
        else:
            g.user = None
            g.lastuserinfo = None

    def login_listener(self, userinfo, token):
        self.before_request()
        user = g.user
        # Username, fullname and email may have changed, so set them again
        user.username = userinfo['username']
        user.fullname = userinfo['fullname']
        user.email = userinfo.get('email')
        user.userinfo = userinfo

        # Watch for username/email conflicts. Remove from any existing user
        # that have the same username or email, for a conflict can only mean
        # that we didn't hear of this change when it happened in LastUser
        olduser = self.usermodel.query.filter_by(username=user.username).first()
        if olduser is not None and olduser.id != user.id:
            olduser.username = None
        olduser = self.usermodel.query.filter_by(email=user.email).first()
        if olduser is not None and olduser.id != user.id:
            olduser.email = None

        user.lastuser_token = token['access_token']
        user.lastuser_token_type = token['token_type']
        user.lastuser_token_scope = token['scope']
        # Commit this so that token info is saved even if the user account is an existing account.
        # This is called before the request is processed by the client app, so there should be no
        # other data in the transaction
        self.db.session.commit()
