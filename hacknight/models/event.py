#! /usr/bin/env python
# -*- coding: utf-8 -*-

from hacknight.models import IdMixin, TimestampMixin, BaseNameMixin, BaseMixin
from hacknight.models import db
from organization import OrganizationMembers

__all__ = ['Event', 'EventDetails', 'EventLocation']
#need to EventTurnOut, EventPayment

class Event(db.Model, BaseNameMixin):
    __tablename__ = 'events'
    created_by = db.Column(db.Integer, db.ForeignKey('organizations_members.id'), nullable=False)
    creator = db.relationship(OrganizationMembers, primaryjoin=creator_by == OrganizationMembers.id, backref=db.backref('organizations_members', cascade='all, delete-orphan'))


class EventDetails(db.Model, BaseMixin):
    __tablename__ = 'events_details'
    event_id = db.Column(db.Integer, db.ForeignKey('events'), nullable=False)
    event = db.relationship(Event, primaryjoin=event_id == Event.id, backref=db.backref('events', cascade='all, delete-orphan'))
    main_event_start_date = db.Column(db.DateTime, nullable=False)
    main_event_end_date = db.Column(db.DateTime, nullable=False, sqlalchemy.CheckConstraint('main_event_end_date > main_event_start_date'))
    hacknight_start_date = db.Column(db.DateTime, nullable=False)
    hacknight_end_date = db.Column(db.DateTime, nullable=False, sqlalchemy.CheckConstraint('hacknight_end_date > hacknight_start_date'))
    maximum_participants = db.Column(db.Integer, default=50, nullable=False, db.CheckConstraint('maximum_participants >= 1'))
    main_event_website = db.Column(db.Unicode(100), nullable=False, unique=True)



class EventLocation(db.Model, IdMixin):
    __tablename__ = 'events_location'
    event_id = db.Column(db.Integer, db.ForeignKey('events'), nullable=False)
    location = db.Column(db.Unicode(100), nullable=False)
    country = db.Column(db.Unicode(50), default=u'india', nullable=False)
