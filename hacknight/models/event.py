# -*- coding: utf-8 -*-

from hacknight.models import db, BaseNameMixin, BaseScopedNameMixin


__all__ = ['Profile', 'Event', 'EVENT_STATUS', 'PROFILE_TYPE']
#need to add EventTurnOut, EventPayment later


class PROFILE_TYPE:
    UNDEFINED = 0
    PERSON = 1
    ORGANIZATION = 2
    EVENTSERIES = 3

profile_types = {
    0: u"Undefined",
    1: u"Person",
    2: u"Organization",
    3: u"Event Series",
    }


class EVENT_STATUS:
    DRAFT = 0
    PUBLISHED = 1
    ACTIVE = 2
    COMPLETED = 3
    CANCELLED = 4
    CLOSED = 5
    REJECTED = 6
    WITHDRAWN = 7


class Profile(BaseNameMixin, db.Model):
    __tablename__ = 'profile'

    userid = db.Column(db.Unicode(22), nullable=False, unique=True)
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    type = db.Column(db.Integer, default=PROFILE_TYPE.UNDEFINED, nullable=False)

    def type_label(self):
        return profile_types.get(self.type, profile_types[0])


class Event(BaseScopedNameMixin, db.Model):
    __tablename__ = 'event'
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship(Profile)
    parent = db.synonym('profile')
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    venue = db.relationship('Venue')
    blurb = db.Column(db.Unicode(250), default=u'', nullable=False)
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    maximum_participants = db.Column(db.Integer, default=0, nullable=False)
    website = db.Column(db.Unicode(250), default=u'', nullable=False)
    status = db.Column(db.Integer, nullable=False, default=EVENT_STATUS.DRAFT)
    ticket_price = db.Column(db.Unicode(250), nullable=False, default=0)

    __table_args__ = (db.UniqueConstraint('name', 'profile_id'),)

    def owner_is(self, user):
        """Check if a user is an owner of this event"""
        return user is not None and self.profile.userid in user.user_organizations_owned_ids()

    def participant_is(self, user):
        from hacknight.models.participant import Participant
        return Participant.get(user, self) is not None

    def confirmed_participant_is(self, user):
        from hacknight.models.participant import Participant, PARTICIPANT_STATUS
        p = Participant.get(user, self)
        return p and p.status == PARTICIPANT_STATUS.CONFIRMED
