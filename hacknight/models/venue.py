# -*- coding: utf-8 -*-

from flask import url_for
from hacknight.models import BaseNameMixin
from hacknight.models import db
from hacknight.models.profile import Profile

__all__ = ['Venue']


class Venue(BaseNameMixin, db.Model):
    __tablename__ = 'venue'
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship(Profile)
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    address1 = db.Column(db.Unicode(80), default=u'', nullable=False)
    address2 = db.Column(db.Unicode(80), default=u'', nullable=False)
    city = db.Column(db.Unicode(30), default=u'', nullable=False)
    state = db.Column(db.Unicode(30), default=u'', nullable=False)
    postcode = db.Column(db.Unicode(20), default=u'', nullable=False)
    country = db.Column(db.Unicode(2), default=u'', nullable=False)
    latitude = db.Column(db.Numeric(8, 5), nullable=True)
    longitude = db.Column(db.Numeric(8, 5), nullable=True)

    def url_for(self, action='view', _external=False):
        if action == 'view':
            return url_for('venue_view', venue=self.name, _external=_external)
