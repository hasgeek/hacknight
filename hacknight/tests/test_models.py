#! /usr/bin/env python
# -*- coding: utf-8 -*-

from hacknight.models import db
from hacknight.tests import Event, EventLocation, User, Location, Project, Mentor, Participant, Payment
from hacknight.tests import MAXIMUM_PROJECT_SIZE
from test_data import EVENTS, EVENT_LOCATIONS, USERS, LOCATIONS, PROJECTS, MENTORS, PARTICIPANTS, PAYMENTS
from nose.tools import ok_, assert_raises
import sqlalchemy

def test_setup():
    global db
    db.create_all()

def test_users():
    global db
    for user in USERS:
        u = User(**user)
        db.session.add(u)
    db.session.commit()
    db.session.add(u)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_events():
    global db
    for event in EVENTS:
        e = Event(**event)
        db.session.add(e)
    db.session.commit()
    db.session.add(e)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_locations():
    global db
    for location in LOCATIONS:
        l = Location(**location)
        db.session.add(l)
    db.session.commit()
    db.session.add(l)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_event_locations():
    for event_location in EVENT_LOCATIONS:
        event = db.session.query(Event).filter_by(name=event_location['name']).first()
        location = db.session.query(Location).filter_by(place=event_location['location']).first()
        el = EventLocation(event_id = event.id, location_id = location.id)
        db.session.add(el)
    db.session.commit()
    db.session.add(el)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())


def test_project():
    for project in PROJECTS:
        event = db.session.query(Event).filter_by(name=project['event_name']).first()
        user = db.session.query(User).filter_by(fullname=project['fullname']).first()
        prjct = Project(userid = user.userid, event_id = event.id, name=project['name'],title=project['title'], description=project['description'], hacknight_bio=project['hacknight_bio'])
        db.session.add(prjct)
    db.session.commit()
    db.session.add(prjct)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_mentor():
    for mentor in MENTORS:
        project = db.session.query(Project).filter_by(name=mentor['project_name']).first()
        user = db.session.query(User).filter_by(fullname=mentor['fullname']).first()
        mntr = Mentor(userid = user.userid, project_id = project.id, mentor_bio=mentor['mentor_bio'])
        db.session.add(mntr)
    db.session.commit()
    db.session.add(mntr)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_participant():
    for participant in PARTICIPANTS:
        project = db.session.query(Project).filter_by(name=participant['project_name']).first()
        user = db.session.query(User).filter_by(fullname=participant['fullname']).first()
        p = Participant(userid = user.userid, project_id = project.id)
        db.session.add(p)
    db.session.commit()
    db.session.add(p)

def test_payments():
    for payment in PAYMENTS:
        event = db.session.query(Event).filter_by(name=payment['event_name']).first()
        user = db.session.query(User).filter_by(fullname=payment['fullname']).first()
        p = Payment(userid = user.userid, event_id = event.id)
        db.session.add(p)
    db.session.commit()
    db.session.add(p)
