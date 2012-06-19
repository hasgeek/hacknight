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


class Participant(BaseMixin, db.Model):
    __tablename__ = 'participant'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event, backref=db.backref('participants', cascade='all, delete-orphan'))
    status = db.Column(db.Integer, default=ParticipantStatus.PENDING, nullable=False)
    mentor = db.Column(db.Boolean, default=False, nullable=False)
    reason_to_join = db.Column(db.UnicodeText, default=u'', nullable=False)
    email = db.Column(db.Unicode(80), default=u'', nullable=False)
    phone_no = db.Column(db.Unicode(15), default=u'', nullable=False)
    job_title = db.Column(db.Unicode(120), default=u'', nullable=False)
    company = db.Column(db.Unicode(1200), default=u'', nullable=False)


    def save_defaults(self):
        user = self.user
        user.email = self.email
        user.phone_no = self.phone_no
        user.job_title = self.job_title
        user.company = self.company

    @classmethod
    def get(cls, user, event):
        return cls.query.filter_by(user_id=user).filter_by(event_id=event).first()






