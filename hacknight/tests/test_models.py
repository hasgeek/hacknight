#! /usr/bin/env python
# -*- coding: utf-8 -*-

from hacknight.models import db
from hacknight.models.user import User
from .test_data import USERS
from nose.tools import ok_, assert_raises
import sqlalchemy

"""def test_setup():
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

def test_profiles():
    global db
    for profile in PROFILES:
        p = Profile(**profile)
        db.session.add(p)
    db.session.commit()
    db.session.add(p)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_event():
    global db
    for event in EVENTS:
        profile = db.session.query(Profile).filter_by(userid=event['userid']).first()
        e = Event(profile_id=profile.id, title=event['title'], start_datetime=event['start_date'], end_datetime=event['end_date'],website=event['website'], name=event['name'])
        db.session.add(e)
    db.session.commit()
    db.session.add(e)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_venue():
    global db
    for venue in VENUES:
        l = Venue(**venue)
        db.session.add(l)
    db.session.commit()
    db.session.add(l)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())


def test_project():
    global db
    for project in PROJECTS:
        event = db.session.query(Event).filter_by(name=project['event_name']).first()
        prjct = Project(event_id = event.id,title=project['title'], description=project['description'], name=project['name'])
        db.session.add(prjct)
    db.session.commit()
    db.session.add(prjct)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())

def test_participant():
    global db
    for participant in PARTICIPANTS:
        user = db.session.query(User).filter_by(fullname=participant['fullname']).first()
        event = db.session.query(Event).filter_by(name=participant['event_name']).first()
        p = Participant(user_id = user.id, event_id = event.id)
        db.session.add(p)
    db.session.commit()
    db.session.add(p)
    assert_raises(sqlalchemy.exceptions.IntegrityError, db.session.commit())


def test_teardown():
    global db
    db.session.expunge_all()
    db.drop_all()
"""
class Test_User():
    def __init__(self):
        self.db = db
        self.db.create_all()

    def testAddUser(self):
        for user in USERS:
            u = User(**user)
            self.db.session.add(u)
        self.db.session.commit()


    def testTearDown(self):
        self.db.session.expunge_all()
        self.db.drop_all()