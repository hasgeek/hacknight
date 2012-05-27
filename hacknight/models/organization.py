# -*- coding: utf-8 -*-

from hacknight.models import IdMixin, TimestampMixin, BaseNameMixin
from hacknight.models import db

__all__ = []

class Organization(db.Model, BaseNameMixin):
    __tablename__ = 'organizations'
    description = db.Column(db.UnicodeText, default=u'', nullable=False)


class OrganizationMembers(db.Model, IdMixin, TimestampMixin)
    __tablename__ = 'organizations_members'
    fullname = db.Column(db.unicode(80), default=u'', nullable=False)


class OrganizationMembersEmail(db.Model, IdMixin, TimestampMixin)
    __tablename__ = 'organizations_members_emails'
    member_id = db.Column(db.Integer, db.ForeignKey('organizations_members.id'), nullable=False)
    member = db.relationship(OrganizationMembers, primaryjoin=member_id == OrganizationMembers.id, backref=db.backref('organizations_members_email', cascade='all, delete-orphan'))

