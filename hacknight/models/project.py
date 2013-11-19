# -*- coding: utf-8- *-

from hacknight.models import BaseMixin, BaseScopedIdNameMixin
from hacknight.models import db
from hacknight.models.event import Event
from hacknight.models.user import User
from hacknight.models.vote import VoteSpace
from hacknight.models.comment import CommentSpace, Comment
from flask import url_for

__all__ = ['Project', 'ProjectMember']


class Project(BaseScopedIdNameMixin, db.Model):
    __tablename__ = 'project'
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relation(Event,
        backref=db.backref('projects', order_by=db.desc('url_id'), cascade='all, delete-orphan'))
    parent = db.synonym('event')

    #: User who is part of this project
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref='projects')

    blurb = db.Column(db.Unicode(250), nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)
    maximum_size = db.Column(db.Integer, default=0, nullable=False)
    #: Is the project owner participating?
    participating = db.Column(db.Boolean, nullable=False, default=True)

    members = db.relationship('ProjectMember', backref='project', uselist=True)

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
    def users(self):
        return set([self.user] + [m.user for m in self.members])

    participants = users

    def owner_is(self, user):
        return user is not None and self.user == user

    def getnext(self):
        return Project.query.filter(Project.event == self.event).filter(
            Project.id != self.id).filter(
            Project.created_at < self.created_at).order_by(db.desc('created_at')).first()

    def getprev(self):
        return Project.query.filter(Project.event == self.event).filter(
            Project.id != self.id).filter(
            Project.created_at > self.created_at).order_by('created_at').first()

    def get_comments(self, reverse=True):
        return sorted(Comment.query.filter_by(commentspace=self.comments, reply_to=None).order_by('created_at').all(),
            key=lambda c: c.votes.count, reverse=reverse)

    def url_for(self, action='view', _external=False):
        if action == 'view':
            return url_for('project_view', profile=self.event.profile.name, event=self.event.name, project=self.url_name, _external=_external)
        elif action == 'edit':
            return url_for('project_edit', profile=self.event.profile.name, event=self.event.name, project=self.url_name, _external=_external)
        elif action == 'delete':
            return url_for('project_delete', profile=self.event.profile.name, event=self.event.name, project=self.url_name, _external=_external)
        elif action == 'voteup':
            return url_for('project_voteup', profile=self.event.profile.name, event=self.event.name, project=self.url_name, _external=_external)
        elif action == 'votedown':
            return url_for('project_votedown', profile=self.event.profile.name, event=self.event.name, project=self.url_name, _external=_external)
        elif action == 'cancelvote':
            return url_for('project_cancelvote', profile=self.event.profile.name, event=self.event.name, project=self.url_name, _external=_external)
        elif action == 'prev':
            return url_for('project_view', profile=self.event.profile.name, event=self.event.name, project=self.getprev().url_name, _external=_external)
        elif action == 'next':
            return url_for('project_view', profile=self.event.profile.name, event=self.event.name, project=self.getnext().url_name, _external=_external)
        elif action == 'join':
            return url_for('project_join', profile=self.event.profile.name, event=self.event.name, project=self.url_name, _external=_external)


class ProjectMember(BaseMixin, db.Model):
    __tablename__ = 'project_member'
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    #: User who created this project
    user_id = db.Column(None, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref('project_memberships', cascade='all, delete-orphan'))

    status = db.Column(db.Integer, nullable=False, default=0)
    role = db.Column(db.Unicode(250), nullable=False, default=u'')

    __table_args__ = (db.UniqueConstraint('project_id', 'user_id'),)

    def permissions(self, user, inherited=None):
        perms = super(ProjectMember, self).permissions(user, inherited)

        if user is not None and user == self.project.user and self.user != user:
            perms.add('remove-member')
        return perms
