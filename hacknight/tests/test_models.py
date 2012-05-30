#! /usr/bin/env python
# -*- coding: utf-8 -*-

from hacknight.models import db
from hacknight.tests import Event, EventLocation, User, Location
from test_data import EVENTS, EVENT_LOCATIONS, USERS, LOCATIONS
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


