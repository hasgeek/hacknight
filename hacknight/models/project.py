# -*- coding: utf-8- *-

from hacknight.models import BaseMixin, BaseScopedIdNameMixin
from hacknight.models import db
from hacknight.models.event import Event
from hacknight.models.participant import Participant
from hacknight.models.vote import Vote, VoteSpace
from hacknight.models.comment import Comment, CommentSpace
__all__ = ['Project', 'ProjectMember']


class Project(BaseScopedIdNameMixin, db.Model):
    __tablename__ = 'project'
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event,
        backref=db.backref('projects', cascade='all, delete-orphan'))
    parent = db.synonym('event')
    description = db.Column(db.UnicodeText, nullable=False)
    objectives = db.Column(db.UnicodeText, nullable=False)
    maximum_size = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)

    members = db.relationship('ProjectMember', backref='project',
                      lazy='dynamic')

    votes_id = db.Column(db.Integer, db.ForeignKey('votespace.id'), nullable=False)
    votes = db.relationship(VoteSpace, uselist=False)

    comments_id = db.Column(db.Integer, db.ForeignKey('commentspace.id'), nullable=False)
    comments = db.relationship(CommentSpace, uselist=False)

    __table_args__ = (db.UniqueConstraint('name', 'event_id'),)

    @property
    def users(self):
        return [m.participant.user for m in self.members]

    @property
    def urlname(self):
        return '%s-%s' % (self.id, self.name)

    def getnext(self):
        return Project.query.filter(Project.event == self.event).filter(
            Project.id != self.id).filter(
            Project.created_at < self.created_at).order_by(db.desc('created_at')).first()

    def getprev(self):
        return Project.query.filter(Project.event == self.event).filter(
            Project.id != self.id).filter(
            Project.created_at > self.created_at).order_by('created_at').first()


class ProjectMember(BaseMixin, db.Model):
    __tablename__ = 'project_member'
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    # project = db.relationship(Project, backref=db.backref('members', cascade='all, delete-orphan'))
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    participant = db.relationship(Participant, backref=db.backref('projects', cascade='all, delete-orphan'))

    status = db.Column(db.Integer, nullable=False, default=0)
    role = db.Column(db.Unicode(250), nullable=False, default=u'')
