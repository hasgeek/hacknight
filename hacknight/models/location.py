# -*- coding: utf-8 -*-

from hacknight.models import BaseNameMixin
from hacknight.models import db

__all__ = ['Venue']


class Venue(db.Model, BaseNameMixin):
    __tablename__ = 'venue'
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    address = db.Column(db.UnicodeText, default=u'', nullable=False)
    latitude = db.Column(db.Numeric, nullable=True)
    longitude = db.Column(db.Numeric, nullable=True)
