#! /usr/bin/env python
# -*- coding: utf-8 -*-

from hacknight.models import db
from hacknight.tests import Event, EventLocation, User, Location, Project, Mentor, Participant, Payment, ParticipantProject
from hacknight.tests import MAXIMUM_PROJECT_SIZE
from test_data import EVENTS, EVENT_LOCATIONS, USERS, LOCATIONS, PROJECTS, MENTORS, PARTICIPANTS, PAYMENTS, PARTICIPANTS_PROJECTS
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
    global db
    for event_location in EVENT_LOCATIONS:
        event = db.session.query(Event).filter_by(name=event_location['name']).first()
        location = db.session.query(Location).filter_by(place=event_location['location']).first()
        el = EventLocation(event_id = event.id, location_id = location.id)
        db.session.add(el)
    db.session.commit()
    db.session.add(el)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())


def test_project():
    global db
    for project in PROJECTS:
        event = db.session.query(Event).filter_by(name=project['event_name']).first()
        user = db.session.query(User).filter_by(fullname=project['fullname']).first()
        prjct = Project(userid = user.userid, event_id = event.id, name=project['name'],title=project['title'], description=project['description'], hacknight_bio=project['hacknight_bio'])
        db.session.add(prjct)
    db.session.commit()
    db.session.add(prjct)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_mentor():
    global db
    for mentor in MENTORS:
        project = db.session.query(Project).filter_by(name=mentor['project_name']).first()
        user = db.session.query(User).filter_by(fullname=mentor['fullname']).first()
        mntr = Mentor(userid = user.userid, project_id = project.id, mentor_bio=mentor['mentor_bio'])
        db.session.add(mntr)
    db.session.commit()
    db.session.add(mntr)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_participant():
    global db
    for participant in PARTICIPANTS:
        event = db.session.query(Event).filter_by(name=participant['event_name']).first()
        user = db.session.query(User).filter_by(fullname=participant['fullname']).first()
        p = Participant(userid = user.userid, event_id = event.id)
        db.session.add(p)
    db.session.commit()
    db.session.add(p)

def test_participant_project():
    global db
    for pp in PARTICIPANTS_PROJECTS:
        project = db.session.query(Project).filter_by(name=pp['project_name']).first()
        participant = db.session.query(Participant).filter_by(userid=pp['userid']).first()
        p = ParticipantProject(pid = participant.id, project_id = project.id)
        db.session.add(p)
    db.session.commit()
    db.session.add(p)

def test_payments():
    global db
    for payment in PAYMENTS:
        event = db.session.query(Event).filter_by(name=payment['event_name']).first()
        user = db.session.query(User).filter_by(fullname=payment['fullname']).first()
        p = Payment(userid = user.userid, event_id = event.id)
        db.session.add(p)
    db.session.commit()
    db.session.add(p)

def test_users_delete():
    global db
    ok_(len(User.query.all()), len(USERS))
    for user in USERS:
        u = db.session.query(User).filter_by(userid=user['userid']).first()
        if u is not None:
            db.session.delete(u)
    ok_(len(User.query.all()), 0)

def test_events_delete():
    global db
    ok_(len(Event.query.all()), len(EVENTS))
    for event in EVENTS:
        e = db.session.query(Event).filter_by(userid=event['name']).first()
        if e is not None:
            # because if delete cascade is present event must have deleted already
            db.session.delete(e)
    ok_(len(Event.query.all()), 0)
    
def test_projects_delete():
    global db
    ok_(len(Project.query.all()), len(PROJECTS))
    for project in PROJECTS:
        p = db.session.query(Project).filter_by(userid=project['name']).first()
        if p is not None:
            db.session.delete(e)
    ok_(len(Project.query.all()), 0)

def test_teardown():
    global db
    db.session.expunge_all()
    db.drop_all()
