#! /usr/bin/env python
# -*- coding: utf-8- *-

from hacknight.models import IdMixin, BaseNameMixin
from hacknight.models import db
from user import User
from event import Event 

__all__ = ['Project', 'Mentor']

#type of project.
PROJECT_TYPE = {
                'normal': 1,
                'proposal': 2,
                'secret': 3,
                'complete': 4,
                'incomplete': 5,
                'called-off': 6
                }

#maximum project team size
MAXIMUM_PROJECT_SIZE = 4

class Project(db.Model, BaseNameMixin):
    __tablename__ = 'projects'
    description = db.Column(db.UnicodeText, nullable = False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    evnt = db.relationship(Event, primaryjoin=event_id == Event.id, backref=db.backref('users', cascade='all, delete-orphan'))
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    creator = db.relationship(User, primaryjoin=userid == User.userid, backref=db.backref('users', cascade='all, delete-orphan'))
   maximum_size = db.Column(db.Integer, default = MAXIMUM_PROJECT_SIZE, nullable = False)
   type = db.column(db.Integer, nullable = False, default = PROJECT_TYPE['normal'])
    hacknight_bio = db.Column(db.UnicodeText, nullable = False)


class Mentor(db.Model, BaseMixin):
    __tablename__ = 'mentors'
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    mentor = db.relationship(User, primaryjoin=userid == User.userid, backref=db.backref('users', cascade='all, delete-orphan'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    evnt = db.relationship(Event, primaryjoin=event_id == Event.id, backref=db.backref('users', cascade='all, delete-orphan'))
    mentor_bio = db.Column(db.UnicodeText, nullable = False)
    
