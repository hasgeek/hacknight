# -*- coding: utf-8 -*-

import datetime
from hacknight.models import db, BaseNameMixin, BaseMixin, Event, User


class EMAIL_CAMPAIGN_STATUS:
    COMPLETED = 1
    PROGRESS = 2


class EmailCampaign(BaseNameMixin, db.Model):
    __tablename__ = "email_campaign"

    event_id = db.Column(None, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event)
    start_datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Integer, default=EMAIL_CAMPAIGN_STATUS.PROGRESS, nullable=False)

    @classmethod
    def get(cls, event):
        return cls.query.filter_by(event=event).first()

    @classmethod
    def sent_for(cls, event):
        email_campaign = cls.get(event=event)
        if email_campaign:
            if email_campaign.status == EMAIL_CAMPAIGN_STATUS.COMPLETED:
                return True
            return False
        return False

    def yet_to_send(self):
        return set(User.subscribed_to_newsletter()) - set([user.user for user in self.users])


class EmailCampaignUser(BaseMixin, db.Model):
    __tablename__ = "email_campaign_user"

    user_id = db.Column(None, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    email_campaign_id = db.Column(None, db.ForeignKey('email_campaign.id'), nullable=False)
    email_campaign = db.relationship(EmailCampaign, backref=db.backref('users', cascade='all, delete-orphan'))
