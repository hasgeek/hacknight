# -*- coding: utf-8- *-

from hacknight.models import BaseMixin, BaseScopedNameMixin
from hacknight.models import db
from hacknight.models.event import Event
from hacknight.models.participant import Participant

__all__ = ['Project', 'ProjectMember']


class Project(db.Model, BaseScopedNameMixin):
    __tablename__ = 'project'
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event,
        backref=db.backref('projects', cascade='all, delete-orphan'))

    description = db.Column(db.UnicodeText, nullable=False)
    maximum_size = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (db.UniqueConstraint('name', 'event_id'),)


class ProjectMember(db.Model, BaseMixin):
    __tablename__ = 'project_member'
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship(Project, backref=db.backref('members', cascade='all, delete-orphan'))
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    participant = db.relationship(Participant, backref=db.backref('projects', cascade='all, delete-orphan'))

    status = db.Column(db.Integer, nullable=False, default=0)
    role = db.Column(db.Unicode(250), nullable=False, default=u'')
