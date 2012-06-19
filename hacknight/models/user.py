# -*- coding: utf-8 -*-

from flask import url_for
from flask.ext.lastuser.sqlalchemy import UserBase
from hacknight.models import db
from hacknight.models.event import Profile

__all__ = ['User']


class User(UserBase, db.Model):
    __tablename__ = 'user'
    email = db.Column(db.Unicode(80), default=u'', nullable=True)
    phone_no = db.Column(db.Unicode(15), default=u'', nullable=True)
    job_title = db.Column(db.Unicode(120), default=u'', nullable=True)
    company = db.Column(db.Unicode(1200), default=u'', nullable=True)

    @property
    def profile_url(self):
        return url_for('profile_view', profile=self.username or self.userid)

    @property
    def profile(self):
        return Profile.query.filter_by(userid=self.userid).first()

    @property
    def profiles(self):
        return [self.profile] + Profile.query.filter(
            Profile.userid.in_(self.organizations_owned_ids())).order_by('title').all()
