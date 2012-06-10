# -*- coding: utf-8- *-

from hacknight.models import BaseMixin, BaseScopedIdNameMixin
from hacknight.models import db
from hacknight.models.event import Event
from hacknight.models.participant import Participant
from hacknight.models.user import User

__all__ = ['VoteSpace', 'Vote']

class VoteSpace(BaseMixin, db.Model):
    __tablename__ = 'votespace'
    type = db.Column(db.Integer, nullable=True)
    count = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, **kwargs):
        super(VoteSpace, self).__init__(**kwargs)
        self.count = 0

    def vote(self, user, votedown=False):
        voteob = Vote.query.filter_by(user=user, votespace=self).first()
        if not voteob:
            voteob = Vote(user=user, votespace=self, votedown=votedown)
            self.count += 1 if not votedown else -1
            db.session.add(voteob)
        else:
            if voteob.votedown != votedown:
                self.count += 2 if not votedown else -2
            voteob.votedown = votedown
        return voteob

    def cancelvote(self, user):
        voteob = Vote.query.filter_by(user=user, votespace=self).first()
        if voteob:
            self.count += 1 if voteob.votedown else -1
            db.session.delete(voteob)

    def getvote(self, user):
        return Vote.query.filter_by(user=user, votespace=self).first()


class Vote(BaseMixin, db.Model):
    __tablename__ = 'vote'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, primaryjoin=user_id == User.id,
        backref=db.backref('votes', cascade="all, delete-orphan"))
    votespace_id = db.Column(db.Integer, db.ForeignKey('votespace.id'), nullable=False)
    votespace = db.relationship(VoteSpace, primaryjoin=votespace_id == VoteSpace.id,
        backref=db.backref('votes', cascade="all, delete-orphan"))
    votedown = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "votespace_id"), {})

