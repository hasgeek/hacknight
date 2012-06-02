# -*- coding: utf-8- *-

from hacknight.models import db, BaseMixin
from hacknight.models.user import User
from hacknight.models.event import Event

<<<<<<< HEAD
__all__ = ['Participant', 'Payment', 'PAYMENT_STATUS', 'PARTICIPANT_STATUS']
=======
__all__ = ['Participant']
>>>>>>> 294af2f9acf09a1af96e46ba6f6bde51b589c179


class Participant(db.Model, BaseMixin):
<<<<<<< HEAD
    __tablename__ = 'participants'
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False, default = PARTICIPANT_STATUS['waiting'])

class Payment(db.Model, BaseMixin):
    __tablename__ = 'payments'
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    evnt = db.relationship(Event, primaryjoin=event_id == Event.id, backref=db.backref('users', cascade='all, delete-orphan'))
    is_paid = db.Column(db.Integer, nullable = False, default = PAYMENT_STATUS['unpaid'])
=======
    __tablename__ = 'participant'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event, backref=db.backref('participants', cascade='all, delete-orphan'))
    status = db.Column(db.Integer, default=0, nullable=False)
    mentor = db.Column(db.Boolean, default=False, nullable=False)
>>>>>>> 294af2f9acf09a1af96e46ba6f6bde51b589c179
