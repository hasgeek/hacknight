# -*- coding: utf-8 -*-

from hacknight.models import IdMixin, TimestampMixin, BaseNameMixin, BaseMixin
from hacknight.models import db

__all__ = ['Organization', 'OrganizationMembers', 'OrganizationMembersEmail', 
           'OrganizationMembersConnection']

class Organization(db.Model, BaseNameMixin):
    __tablename__ = 'organizations'
    description = db.Column(db.UnicodeText, default=u'', nullable=False)


class OrganizationMembers(db.Model, BaseMixin):
    __tablename__ = 'organizations_members'
    fullname = db.Column(db.Unicode(80), unique=True, nullable=False)


class OrganizationMembersEmail(db.Model, BaseMixin):
    __tablename__ = 'organizations_members_emails'
    member_id = db.Column(db.Integer, db.ForeignKey('organizations_members.id'), nullable=False)
    member = db.relationship(OrganizationMembers, primaryjoin=member_id == OrganizationMembers.id, backref=db.backref('organizations_members_email', cascade='all, delete-orphan'))
    is_primary = db.Column(db.Boolean, nullable=False, default = False)


class OrganizationMembersConnection(db.Model, BaseMixin):
    __tablename__ = 'organizations_members_connections'
    member_id = db.Column(db.Integer, db.ForeignKey('organizations_members.id'), nullable=False)
    member = db.relationship(OrganizationMembers, primaryjoin=member_id == OrganizationMembers.id, backref=db.backref('organizations_members_connections', cascade='all, delete-orphan'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations_members.id'), nullable=False)
    
