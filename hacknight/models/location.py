#! /usr/bin/env python
# -*- coding: utf-8 -*-

from hacknight.models import BaseMixin
from hacknight.models import db

__all__ = ['Location']

class Location(db.Model, BaseMixin):
    __tablename__ = 'locations'
    place = db.Column(db.Unicode(250), nullable = False, unique = True)
    country = db.Column(db.Unicode(50), default=u'india', nullable=False)
