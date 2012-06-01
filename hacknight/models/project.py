#! /usr/bin/env python
# -*- coding: utf-8- *-

from hacknight.models import IdMixin, BaseNameMixin, BaseMixin
from hacknight.models import db
from user import User
from event import Event 

__all__ = ['Project', 'Mentor', 'PROJECT_TYPE', 'MAXIMUM_PROJECT_SIZE']

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
    event = db.relationship(Event, primaryjoin=event_id == Event.id, backref=db.backref('events', cascade='all, delete-orphan'))
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    maximum_size = db.Column(db.Integer, default = MAXIMUM_PROJECT_SIZE, nullable = False)
    type = db.Column(db.Integer, nullable = False, default = PROJECT_TYPE['normal'])
    hacknight_bio = db.Column(db.UnicodeText)


class Mentor(db.Model, BaseMixin):
    __tablename__ = 'mentors'
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship(Project, primaryjoin=project_id == Project.id, backref=db.backref('projects', cascade='all, delete-orphan'))
    mentor_bio = db.Column(db.UnicodeText)
    
