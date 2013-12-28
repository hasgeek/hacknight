# -*- coding: utf-8 -*-

import datetime
from hacknight.models import db, BaseNameMixin, BaseMixin, Event, User


class EmailCampaign(BaseNameMixin, db.Model):
    __tablename__ = "email_campaign"

    event_id = db.Column(None, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event)
    start_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=True)

    @classmethod
    def sent_for(cls, event):
        if cls.query.filter_by(event=event).first():
            return True
        return False


class EmailCampaignUser(BaseMixin, db.Model):
    __tablename__ = "email_campaign_user"

    user_id = db.Column(None, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    email_campaign_id = db.Column(None, db.ForeignKey('email_campaign.id'), nullable=False)
    email_campaign = db.relationship(EmailCampaign, backref=db.backref('users', cascade='all, delete-orphan'))
