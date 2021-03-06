# -*- coding: utf-8- *-

from hacknight.models import db, BaseMixin
from hacknight.models.user import User
from hacknight.models.event import Event


__all__ = ['Participant', 'PARTICIPANT_STATUS']


class PARTICIPANT_STATUS:
    PENDING = 0
    WL = 1
    CONFIRMED = 2
    REJECTED = 3
    WITHDRAWN = 4
    ATTENDED = 5


class Participant(BaseMixin, db.Model):
    __tablename__ = 'participant'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event, backref=db.backref('participants', cascade='all, delete-orphan'))
    status = db.Column(db.Integer, default=PARTICIPANT_STATUS.PENDING, nullable=False)
    mentor = db.Column(db.Boolean, default=False, nullable=False)
    reason_to_join = db.Column(db.UnicodeText, default='', nullable=False)
    email = db.Column(db.Unicode(80), default='', nullable=False)
    phone_no = db.Column(db.Unicode(15), default='', nullable=False)
    job_title = db.Column(db.Unicode(120), default='', nullable=False)
    company = db.Column(db.Unicode(1200), default='', nullable=False)
    skill_level = db.Column(db.Unicode(120), default='', nullable=False)

    NON_CONFIRMED_STATUSES = (PARTICIPANT_STATUS.PENDING, PARTICIPANT_STATUS.WL)

    @classmethod
    def unconfirmed_for(cls, event):
        return cls.query.filter(cls.status.in_([PARTICIPANT_STATUS.PENDING, PARTICIPANT_STATUS.WL]), cls.event == event).all()

    def save_defaults(self):
        user = self.user
        user.phone_no = self.phone_no
        user.job_title = self.job_title
        user.company = self.company

    def confirm(self):
        self.status = PARTICIPANT_STATUS.CONFIRMED

    @classmethod
    def get(cls, user, event):
        return cls.query.filter_by(user=user).filter_by(event=event).first()

    @property
    def is_participating(self):
        return self.status in (PARTICIPANT_STATUS.CONFIRMED, PARTICIPANT_STATUS.ATTENDED)
