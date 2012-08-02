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
        db.create_all()
        #test user insertion
        for user_data in USERS:
            u = User(**user_data)
            db.session.add(u)
        db.session.commit()
        #test profile insertion
        for profile_data in PROFILES:
            p = Profile(**profile_data)
            db.session.add(p)
        db.session.commit()
        #test venue insertion
        profile = db.session.query(Profile).first()
        for venue_data in VENUES:
            v = Venue(profile=profile, **venue_data)
            db.session.add(v)
        db.session.commit()
        #test event insertion
        venue = db.session.query(Venue).first()
        for event_data in EVENTS:
            e = Event(profile=profile, venue=venue, **event_data)
            db.session.add(e)
        db.session.commit()
        #test participant insertion
        event = db.session.query(Event).first()
        user = db.session.query(User).first()
        for participant_data in PARTICIPANTS:
            p = Participant(user=user, event=event, **participant_data)
            db.session.add(p)
        db.session.commit()
        #test project insertion
        participant = db.session.query(Participant).first()
        for project_data in PROJECTS:
            p = Project(participant=participant, event=participant.event, **project_data)
            p.votes.vote(participant.user)
            db.session.add(p)
        db.session.commit()
        #test project member
        projects = db.session.query(Project).all()
        for project in projects:
            project_member = ProjectMember(project=project, participant=project.participant)
            db.session.add(project_member)
        db.session.commit()

    def test_app_logic(self):
        """
            Voteup/votedown/cancelvote for comments, projects
        """
        #test voteup votedown cancelvote
        projects = db.session.query(Project).all()
        project = projects[0]
        #test votedown

        event = db.session.query(Event).first()
        user = db.session.query(User).first()
        project.votes.vote(user, votedown=True)
        #print project.votes.count
        self.assertEqual(project.votes.count, -1)
        #test cancel vote
        project.votes.cancelvote(user)
        self.assertEqual(project.votes.count, 0)
        #test voteup
        project.votes.vote(user, votedown=False)
        #print project.votes.count
        self.assertEqual(project.votes.count, 2)
        #add comment to project
        for comment in COMMENTS:
            comment = Comment(commentspace=project.comments, user=user, message=comment['message'], message_html=comment['message_html'])
            self.assertEqual(project.comments.count, 0)
            project.comments.count += 1
            comment.votes.vote(user)  # Vote for your own comment
            comment.make_id()
            db.session.add(comment)
        db.session.commit()
        self.assertEqual(project.comments.count, 1)

        comments_length = len(db.session.query(Comment).all())
        self.assertEqual(comments_length, 1)

        for rcomment in REPLY_COMMENTS:
            new_comment = Comment(commentspace=project.comments, user=user, message=rcomment['message'], message_html=rcomment['message_html'], reply_to_id=comment.id)
            project.comments.count += 1
            new_comment.votes.vote(user)  # Vote for your own comment
            new_comment.make_id()
            db.session.add(new_comment)
        db.session.commit()
        self.assertEqual(project.comments.count, 2)

        comments = db.session.query(Comment).all()
        comment = comments[0]

        #votedown the comment
        self.assertEqual(comment.votes.count, 1)
        comment.votes.vote(user, votedown=True)
        db.session.add(comment)
        db.session.commit()
        self.assertEqual(comment.votes.count, -1)

        #voteup the comment
        comment.votes.vote(user, votedown=False)
        db.session.add(comment)
        db.session.commit()
        self.assertEqual(comment.votes.count, 1)

        comment.votes.cancelvote(user)
        db.session.add(comment)
        db.session.commit()
        self.assertEqual(comment.votes.count, 0)

        #delete the comment
        comment.delete()
        #print project.comments.count
        db.session.add(comment)
        db.session.commit()
        self.assertEqual(comment.status, COMMENTSTATUS.DELETED)

        for sponsor in SPONSORS:
            sponsor = Sponsor(event_id=event.id, **sponsor)
            db.session.add(sponsor)
        db.session.commit()

    def test_delete(self):
        """
            All Deletion operation here
        """
        #Delete all users
        users = db.session.query(User).all()
        users_length = len(users)
        self.assertEqual(users_length, 1)
        for user in users:
            db.session.delete(user)
        db.session.commit()
        total_users_after_deletion = len(db.session.query(User).all())
        self.assertEqual(total_users_after_deletion, 0)

        #Delete all Events
        events = db.session.query(Event).all()
        total_users = len(events)
        self.assertEqual(total_users, 1)
        for event in events:
            db.session.delete(event)
        db.session.commit()
        events = db.session.query(Event).all()
        total_events_after_deletion = len(events)
        self.assertEqual(total_events_after_deletion, 0)

        #Delete all profiles
        profiles = db.session.query(Profile).all()
        total_profiles = len(profiles)
        self.assertEqual(total_profiles, 1)
        for profile in profiles:
            db.session.delete(profile)
        db.session.commit()
        profiles = db.session.query(Profile).all()
        total_profiles_after_deletion = len(profiles)
        self.assertEqual(total_profiles_after_deletion, 0)

        #Delete Venues
        venues = db.session.query(Venue).all()
        total_venues = len(venues)
        self.assertEqual(total_venues, 1)
        for venue in venues:
            db.session.delete(venue)
        db.session.commit()
        venues = db.session.query(Venue).all()
        total_venues_after_deletion = len(venues)
        self.assertEqual(total_venues_after_deletion, 0)

        #from hereon checking cascading delete
        total_participants = len(db.session.query(Participant).all())
        self.assertEqual(total_participants, 0)

        total_projects = len(db.session.query(Project).all())
        self.assertEqual(total_projects, 0)

        total_sponsors = len(db.session.query(Sponsor).all())
        self.assertEqual(total_sponsors, 0)

    def tearDown(self):
        db.session.expunge_all()
        db.drop_all()


class TestBase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        configureapp(app, 'test')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


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
