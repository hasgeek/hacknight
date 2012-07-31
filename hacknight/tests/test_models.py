#! /usr/bin/env python
# -*- coding: utf-8 -*-

from hacknight.models import db
from hacknight.models.user import User
from hacknight.models.event import Profile, Event
from hacknight.models.venue import Venue
from hacknight.models.participant import Participant
from hacknight.models.project import Project, ProjectMember
from hacknight.models.comment import Comment, COMMENTSTATUS
from hacknight.models.sponsor import Sponsor
from test_data import USERS, PROFILES, VENUES, EVENTS, PARTICIPANTS, PROJECTS, SPONSORS, COMMENTS, REPLY_COMMENTS
import unittest
from flask.ext.testing import TestCase, Twill
from hacknight import configureapp, app


class TestDB(unittest.TestCase):
    """ Test Case to test all models"""
    def setUp(self):
        self.db = db
        self.db.create_all()

    def test_all(self):
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
        #test voteup votedown cancelvote
        project = projects[0]
        #test votedown
        project.votes.vote(user, votedown=True)
        #print project.votes.count
        assert project.votes.count == -1
        #test cancel vote
        project.votes.cancelvote(user)
        assert project.votes.count == 0
        #test voteup
        project.votes.vote(user, votedown=False)
        #print project.votes.count
        assert project.votes.count == 2
        #add comment to project
        for comment in COMMENTS:
            comment = Comment(commentspace=project.comments, user=user, message=comment['message'], message_html=comment['message_html'])
            assert project.comments.count == 0
            project.comments.count += 1
            comment.votes.vote(user)  # Vote for your own comment
            comment.make_id()
            self.db.session.add(comment)
        self.db.session.commit()
        assert project.comments.count == 1

        comments = db.session.query(Comment).all()
        assert len(comments) == 1

        for rcomment in REPLY_COMMENTS:
            new_comment = Comment(commentspace=project.comments, user=user, message=rcomment['message'], message_html=rcomment['message_html'], reply_to_id=comment.id)
            project.comments.count += 1
            new_comment.votes.vote(user)  # Vote for your own comment
            new_comment.make_id()
            self.db.session.add(new_comment)
        self.db.session.commit()
        assert project.comments.count == 2

        comments = db.session.query(Comment).all()
        comment = comments[0]

        #votedown the comment
        assert comment.votes.count == 1
        comment.votes.vote(user, votedown=True)
        self.db.session.add(comment)
        self.db.session.commit()
        assert comment.votes.count == -1

        #voteup the comment
        comment.votes.vote(user, votedown=False)
        self.db.session.add(comment)
        self.db.session.commit()
        assert comment.votes.count == 1

        comment.votes.cancelvote(user)
        self.db.session.add(comment)
        self.db.session.commit()
        assert comment.votes.count == 0

        #delete the comment
        comment.delete()
        #print project.comments.count
        self.db.session.add(comment)
        self.db.session.commit()
        assert comment.status == COMMENTSTATUS.DELETED

        for sponsor in SPONSORS:
            sponsor = Sponsor(event_id=event.id, **sponsor)
            self.db.session.add(sponsor)
        self.db.session.commit()

        """
            All Deletion operation here
        """
        #Delete all users
        users = self.db.session.query(User).all()
        assert len(users) == 1
        for user in users:
            self.db.session.delete(user)
        self.db.session.commit()
        assert len(self.db.session.query(User).all()) == 0

        #Delete all Events
        events = self.db.session.query(Event).all()
        assert len(events) == 1
        for event in events:
            self.db.session.delete(event)
        self.db.session.commit()
        events = self.db.session.query(Event).all()
        assert len(events) == 0

        #Delete all profiles
        profiles = self.db.session.query(Profile).all()
        assert len(profiles) == 1
        for profile in profiles:
            self.db.session.delete(profile)
        self.db.session.commit()
        profiles = self.db.session.query(Profile).all()
        assert len(events) == 0

        #Delete Venues
        venues = self.db.session.query(Venue).all()
        assert len(venues) == 1
        for venue in venues:
            self.db.session.delete(venue)
        self.db.session.commit()
        venues = self.db.session.query(Venue).all()
        assert len(venues) == 0

        #from hereon checking cascading delete
        participants = self.db.session.query(Participant).all()
        assert len(participants) == 0

        projects = self.db.session.query(Project).all()
        assert len(projects) == 0

        sponsors = self.db.session.query(Sponsor).all()
        assert len(sponsors) == 0

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
