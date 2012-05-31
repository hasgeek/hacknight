#! /usr/bin/env python
# -*- coding: utf-8- *-

from hacknight.models import IdMixin, BaseMixin
from hacknight.models import db
from user import User
from project import Project
from event import Event 

__all__ = ['Participant', 'Payment']

PAYMENT_TYPE = {
                'paid': 1, 
                'unpaid': 2
                }

PARTICIPANT_STATUS = {
                      'selected': 1,
                      'waiting': 2,
                      'rejected': 3
                      }
    

class Participant(db.Model, BaseMixin):
    __tablename__ = 'participants'
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    usr = db.relationship(User, primaryjoin=userid == User.userid, backref=db.backref('users', cascade='all, delete-orphan'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship(Project, primaryjoin=project_id == Project.id, backref=db.backref('projects', cascade='all, delete-orphan'))
    status = db.Column(db.Integer, nullable=False, default = PARTICIPANT_STATUS['waiting'])

class Payment(db.Model, BaseMixin):
    __tablename__ = 'payments'
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    usr = db.relationship(User, primaryjoin=userid == User.userid, backref=db.backref('users', cascade='all, delete-orphan'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    evnt = db.relationship(Event, primaryjoin=event_id == Event.id, backref=db.backref('users', cascade='all, delete-orphan'))
    is_paid = db.Column(db.Integer, nullable = False, default = PAYMENT_STATUS['unpaid'])
