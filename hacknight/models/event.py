# -*- coding: utf-8 -*-

from flask import url_for
from flask.ext.lastuser.sqlalchemy import ProfileMixin
from sqlalchemy.orm import deferred
from hacknight.models import db, BaseNameMixin, BaseScopedNameMixin, BaseMixin

__all__ = ['Profile', 'Event', 'EVENT_STATUS', 'PROFILE_TYPE', 'EventRedirect']
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


class Profile(ProfileMixin, BaseNameMixin, db.Model):
    __tablename__ = 'profile'

    userid = db.Column(db.Unicode(22), nullable=False, unique=True)
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    type = db.Column(db.Integer, default=PROFILE_TYPE.UNDEFINED, nullable=False)

    def type_label(self):
        return profile_types.get(self.type, profile_types[0])

    def url_for(self, action='view', _external=True):
        if action == 'view':
            return url_for('profile_view', profile=self.name, _external=_external)
        elif action == 'new-event':
            return url_for('event_new', profile=self.name, _external=_external)


class Event(BaseScopedNameMixin, db.Model):
    __tablename__ = 'event'
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship(Profile)
    parent = db.synonym('profile')
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    venue = db.relationship('Venue')
    blurb = db.Column(db.Unicode(250), default=u'', nullable=False)
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    apply_instructions = db.Column(db.UnicodeText, default=u'', nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    maximum_participants = db.Column(db.Integer, default=0, nullable=False)
    website = db.Column(db.Unicode(250), default=u'', nullable=False)
    status = db.Column(db.Integer, nullable=False, default=EVENT_STATUS.DRAFT)
    ticket_price = db.Column(db.Unicode(250), nullable=False, default=u'')
    confirmation_message = deferred(db.Column(db.UnicodeText, nullable=False, default=u''))
    confirmation_message_text = deferred(db.Column(db.UnicodeText, nullable=False, default=u''))
    waitlisted_message = deferred(db.Column(db.UnicodeText, nullable=False, default=u''))
    waitlisted_message_text = deferred(db.Column(db.UnicodeText, nullable=False, default=u''))
    rejected_message = deferred(db.Column(db.UnicodeText, nullable=False, default=u''))
    rejected_message_text = deferred(db.Column(db.UnicodeText, nullable=False, default=u''))
    pending_message = deferred(db.Column(db.UnicodeText, nullable=False, default=u''))
    pending_message_text = deferred(db.Column(db.UnicodeText, nullable=False, default=u''))
    irc_channel_url = db.Column(db.Unicode(250), default=u'', nullable=False)

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

    def confirmed_participants_count(self):
        from hacknight.models.participant import Participant, PARTICIPANT_STATUS
        return Participant.query.filter_by(status=PARTICIPANT_STATUS.CONFIRMED, event=self).count()

    def permissions(self, user, inherited=None):
        perms = super(Event, self).permissions(user, inherited)
        if user is not None and user.userid == self.profile.userid or self.status in [EVENT_STATUS.PUBLISHED,
            EVENT_STATUS.ACTIVE, EVENT_STATUS.COMPLETED, EVENT_STATUS.CANCELLED,
            EVENT_STATUS.CLOSED]:
            perms.add('view')
        if user is not None and self.profile.userid in user.user_organizations_owned_ids():
            perms.add('edit')
            perms.add('delete')
            perms.add('send-email')
        return perms

    def url_for(self, action='view', _external=False):
        if action == 'view':
            return url_for('event_view', profile=self.profile.name, event=self.name, _external=_external)
        elif action == 'edit':
            return url_for('event_edit', profile=self.profile.name, event=self.name, _external=_external)
        elif action == 'delete':
            return url_for('event_delete', profile=self.profile.name, event=self.name, _external=_external)
        elif action == 'new-project':
            return url_for('project_new', profile=self.profile.name, event=self.name, _external=_external)
        elif action == 'apply':
            return url_for('event_apply', profile=self.profile.name, event=self.name, _external=_external)
        elif action == 'update':
            return url_for('event_update_participant_status', profile=self.profile.name, event=self.name, _external=_external)
        elif action == 'withdraw':
            return url_for('event_withdraw', profile=self.profile.name, event=self.name, _external=_external)
        elif action == 'open':
            return url_for('event_open', profile=self.profile.name, event=self.name, _external=_external)
        elif action == 'export':
            return url_for('event_export', profile=self.profile.name, event=self.name, _external=_external)
        elif action == 'send_email':
            return url_for('event_send_email', profile=self.profile.name, event=self.name, _external=_external)
        elif action == 'email_template':
            return url_for('email_template_form', profile=self.profile.name, event=self.name, _external=_external)


class EventRedirect(BaseMixin, db.Model):
    __tablename__ = "event_redirect"

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship(Profile)

    name = db.Column(db.Unicode(250), nullable=False)
    event_id = db.Column(None, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event, backref=db.backref('redirects', cascade='all, delete-orphan'))

    __table_args__ = (db.UniqueConstraint(profile_id, name),)
