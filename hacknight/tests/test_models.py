#! /usr/bin/env python
# -*- coding: utf-8 -*-

from hacknight.models import db
from hacknight.models.user import User
from hacknight.models.event import Profile, Event
from hacknight.models.venue import Venue
from hacknight.models.participant import Participant
from hacknight.models.project import Project, ProjectMember
from hacknight.models.sponsor import Sponsor
from test_data import USERS, PROFILES, VENUES, EVENTS, PARTICIPANTS, PROJECTS, SPONSORS
import unittest
from flask.ext.testing import TestCase, Twill
from hacknight import configureapp, app


class TestDB(unittest.TestCase):
    """ Test Case to test all models"""
    def setUp(self):
        self.db = db
        self.db.create_all()

    def test_add(self):
        """
            All DB insertion is performed here.
        """
        #test user insertion
        for user in USERS:
            u = User(**user)
            self.db.session.add(u)
        self.db.session.commit()
        #test profile insertion
        for profile in PROFILES:
            p = Profile(**profile)
            self.db.session.add(p)
        self.db.session.commit()
        #test venue insertion
        profile = db.session.query(Profile).first()
        for venue in VENUES:
            v = Venue(profile_id=profile.id, **venue)
            self.db.session.add(v)
        self.db.session.commit()
        #test event insertion
        venue = db.session.query(Venue).first()
        for event in EVENTS:
            e = Event(profile_id=profile.id, venue_id=venue.id, **event)
            self.db.session.add(e)
        self.db.session.commit()
        #test participant insertion
        event = db.session.query(Event).first()
        user = db.session.query(User).first()
        for participant in PARTICIPANTS:
            p = Participant(user_id=user.id, event_id=event.id, **participant)
            self.db.session.add(p)
        self.db.session.commit()
        #test project insertion
        participant = self.db.session.query(Participant).first()
        for project in PROJECTS:
            p = Project(participant_id=participant.id, event_id=participant.event_id, **project)
            p.votes.vote(participant.user)
            self.db.session.add(p)
        self.db.session.commit()
        #test project member
        projects = db.session.query(Project).all()
        for project in projects:
            project_member = ProjectMember(project=project, participant=project.participant)
            self.db.session.add(project_member)
        self.db.session.commit()
        for sponsor in SPONSORS:
            sponsor = Sponsor(event_id=event.id, **sponsor)
            self.db.session.add(sponsor)
        self.db.session.commit()

    def test_delete(self):
        #Delete all users
        users = self.db.session.query(User).all()
        for user in users:
            self.db.session.delete(user)
        self.db.session.commit()
        #Delete all Events
        events = self.db.session.query(Event).all()
        for event in events:
            self.db.session.delete(event)
        self.db.session.commit()
        #Delete all profiles
        profiles = self.db.session.query(Profile).all()
        for profile in profiles:
            self.db.session.delete(profile)
        self.db.session.commit()
        #Delete Venues
        venues = self.db.session.query(Event).all()
        for venue in venues:
            self.db.session.delete(venue)
        self.db.session.commit()
        #Delete Participants
        participants = self.db.session.query(Participant).all()
        for participant in participants:
            self.db.session.delete(participant)
        self.db.session.commit()
        #Delete Projects
        projects = self.db.session.query(Project).all()
        for project in projects:
            self.db.session.delete(project)
        self.db.session.commit()
        #Delete sponsors
        sponsors = self.db.session.query(Sponsor).all()
        for sponsor in sponsors:
            self.db.session.delete(sponsor)
        self.db.session.commit()

    def tearDown(self):
        self.db.session.expunge_all()
        self.db.drop_all()


class TestBase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        configureapp(app, 'test')
        return app

    def setUp(self):
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()


class TestWorkFlow(TestBase):
    def test_index(self):
        with Twill(self.app, port=8000) as t:
            t.browser.go(t.url('/'))

    def test_venue(self):
        with Twill(self.app, port=8000) as t:
            t.browser.go(t.url('/venue'))

    def test_event_new(self):
        with Twill(self.app, port=8000) as t:
            b = t.browser
            b.go(t.url('/someuser/new'))
            assert b.get_code() == 404  # while creating a new event, login is required, this redirects to lastuser login, since lastuser isn't up we should get 404
