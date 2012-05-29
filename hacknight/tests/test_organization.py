#! /usr/bin/env python
# -*- coding: utf-8 -*-

from hacknight.models import db
from hacknight.tests import Organization, OrganizationMembers, OrganizationMembersEmail, OrganizationMembersConnection
from hacknight.tests import Event, EventDetails, EventLocation
from test_data import ORGANIZATION, ORGANIZATION_MEMBERS, ORGANIZATION_EMAILS, ORGANIZATION_MEMBERS_CONNECTION
from test_data import EVENTS, EVENTS_DETAILS, EVENTS_LOCATION
from nose.tools import ok_, assert_raises
import sqlalchemy

def test_setup():
    global db
    db.create_all()

def test_organization():
    global db
    for organization in ORGANIZATION:
        org = Organization(**organization)
        db.session.add(org)
    db.session.commit()
    db.session.add(org)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_organization_members():
    global db
    for member in ORGANIZATION_MEMBERS:
        m = OrganizationMembers(fullname=member)
        db.session.add(m)
    db.session.commit()
    db.session.add(m)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_organization_emails():
    global db
    for details in ORGANIZATION_EMAILS:
        result = db.session.query(OrganizationMembers).filter_by(fullname=details['fullname']).first()
        add_email = OrganizationMembersEmail(member_id=result.id, email=details['email'], is_primary=details['is_primary'])
        db.session.add(add_email)
    db.session.commit()
    db.session.add(add_email)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_organization_members_connection():
    global db
    for connection in ORGANIZATION_MEMBERS_CONNECTION:
        member = db.session.query(OrganizationMembers).filter_by(fullname=connection['member_name']).first()
        org = db.session.query(Organization).filter_by(name=connection['organization_name']).first()
        item = OrganizationMembersConnection(member_id=member.id, organization_id=org.id)
    db.session.commit()
    
def test_events():
    global db
    for event in EVENTS:
        e = Event(**events)
        db.session.add(e)
    db.session.commit()
    db.session.add(e)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())
