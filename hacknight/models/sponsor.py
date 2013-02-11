# -*- coding: utf-8- *-

from flask import url_for
from hacknight.models import BaseScopedNameMixin
from hacknight.models import db
from hacknight.models.event import Event

__all__ = ['Sponsor']


class Sponsor(BaseScopedNameMixin, db.Model):
    __tablename__ = 'sponsor'
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    event = db.relation(Event,
        backref=db.backref('sponsors', cascade='all, delete-orphan'))
    parent = db.synonym('event')

    website = db.Column(db.Unicode(250), nullable=True)
    image_url = db.Column(db.Unicode(250), nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)

    __table_args__ = (db.UniqueConstraint('name', 'event_id'),)

    def url_for(self, action='view', _external=False):
        if action == 'view':
            return url_for('sponsor_view', profile=self.event.profile.name, event=self.event.name, sponsor=self.name)
