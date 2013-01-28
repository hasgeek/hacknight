# -*- coding: utf-8- *-

from hacknight.models import BaseMixin, BaseScopedIdNameMixin
from hacknight.models import db
from hacknight.models.event import Event
from hacknight.models.user import User
from hacknight.models.participant import Participant
from hacknight.models.vote import VoteSpace
from hacknight.models.comment import CommentSpace

__all__ = ['Project', 'ProjectMember']


class Project(BaseScopedIdNameMixin, db.Model):
    __tablename__ = 'project'
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relation(Event,
        backref=db.backref('projects', cascade='all, delete-orphan'))
    parent = db.synonym('event')

    #: User who created this project
    user_id = db.Column(None, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)

    blurb = db.Column(db.Unicode(250), nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)
    maximum_size = db.Column(db.Integer, default=0, nullable=False)
    #: Is the project owner participating?
    participating = db.Column(db.Boolean, nullable=False, default=True)

    members = db.relationship('ProjectMember', backref='project',
                      lazy='dynamic')

    votes_id = db.Column(db.Integer, db.ForeignKey('votespace.id'), nullable=False)
    votes = db.relationship(VoteSpace, uselist=False)

    comments_id = db.Column(db.Integer, db.ForeignKey('commentspace.id'), nullable=False)
    comments = db.relationship(CommentSpace, uselist=False)

    __table_args__ = (db.UniqueConstraint('url_id', 'event_id'),)

    def __init__(self, **kwargs):
        super(Project, self).__init__(**kwargs)
        if not self.votes:
            self.votes = VoteSpace(type=0)
        if not self.comments:
            self.comments = CommentSpace()

    @property
    def user(self):
        return self.participant.user

    @property
    def participants(self):
        return set([self.participant] + [m.participant for m in self.members])

    @property
    def users(self):
        return set([self.user] + [m.participant.user for m in self.members])

    def owner_is(self, user):
        return self.user == user

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
    #: User who created this project
    user_id = db.Column(None, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)

    status = db.Column(db.Integer, nullable=False, default=0)
    role = db.Column(db.Unicode(250), nullable=False, default=u'')

    __table_args__ = (db.UniqueConstraint('project_id', 'user_id'),)
