# -*- coding: utf-8- *-

from hacknight.models import db, BaseMixin
from hacknight.models.user import User
from hacknight.models.event import Event

__all__ = ['Participant', 'ParticipantStatus']

class ParticipantStatus:
    PENDING = 0
    WL = 1
    CONFIRMED = 2
    REJECTED = 3
    WITHDRAWN = 4
    OWNER = 5

class Participant(BaseMixin, db.Model):
    __tablename__ = 'participant'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event, backref=db.backref('participants', cascade='all, delete-orphan'))
    status = db.Column(db.Integer, default=ParticipantStatus.PENDING, nullable=False)
    mentor = db.Column(db.Boolean, default=False, nullable=False)



