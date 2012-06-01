#! /usr/bin/env python
# -*- coding: utf-8 -*-

from hacknight.models import IdMixin, BaseNameMixin
from hacknight.models import db
from user import User

__all__ = ['Event', 'EventLocation']
#need to EventTurnOut, EventPayment

#total hacknight size
MAXIMUM_PARTICIPANTS = 50

class Event(db.Model, BaseNameMixin):
    __tablename__ = 'events'
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    evnt_creator = db.relationship(User, primaryjoin=userid == User.userid, backref=db.backref('users', cascade='all, delete-orphan'))
    main_event_start_date = db.Column(db.DateTime, nullable=False)
    main_event_end_date = db.Column(db.DateTime, nullable=False)
    hacknight_start_date = db.Column(db.DateTime, nullable=False)
    hacknight_end_date = db.Column(db.DateTime, nullable=False)
    maximum_participants = db.Column(db.Integer, default=MAXIMUM_PARTICIPANTS, nullable=False)
    main_event_website = db.Column(db.Unicode(100), nullable=False, unique=True)


class EventLocation(db.Model, IdMixin):
    __tablename__ = 'events_location'
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False, unique = True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False, unique = True)
