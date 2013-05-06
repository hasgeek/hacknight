# -*- coding: utf-8 -*-

from flask import url_for
from hacknight.models import db, BaseNameMixin

__all__ = ['Profile', 'PROFILE_TYPE']


class PROFILE_TYPE:
    UNDEFINED = 0
    PERSON = 1
    ORGANIZATION = 2
    EVENTSERIES = 3

profile_types = {
    0: u"Undefined",
    1: u"Person",
    2: u"Organization",
    3: u"Event Series",
    }


class Profile(BaseNameMixin, db.Model):
    __tablename__ = 'profile'

    userid = db.Column(db.Unicode(22), nullable=False, unique=True)
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    type = db.Column(db.Integer, default=PROFILE_TYPE.UNDEFINED, nullable=False)

    def type_label(self):
        return profile_types.get(self.type, profile_types[0])

    def url_for(self, action='view', _external=True):
        if action == 'view':
            return url_for('profile_view', profile=self.name, _external=_external)
        elif action == 'new-event':
            return url_for('event_new', profile=self.name, _external=_external)
