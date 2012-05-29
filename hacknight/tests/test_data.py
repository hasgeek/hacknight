#! /usr/bin/env python
# -*- coding: utf-8 -*-

ORGANIZATION = [{'name': 'hasgeek', 'title': "Come to our events to meet like-minded people", "description": "We are @hasgeek.We made DocType HTML5, AndroidCamp, Scaling PHP in the Cloud, JSFoo, Droidcon, the Cartonama Workshop and Meta Refresh. "}, {'name': 'pycon', 'title': 'Python Conference India', 'description': 'governing body of pycon'}]

ORGANIZATION_MEMBERS = ['kiran', 'sajjad anwar', 'nigel']

ORGANIZATION_EMAILS = [{'fullname': 'kiran', 'email': 'kiran@hasgeek.com', 'is_primary': True}, {'fullname': 'kiran', 'email': 'kiran@gmail.com', 'is_primary': False}]

ORGANIZATION_MEMBERS_CONNECTION = [{'member_name': 'kiran', 'organization_name': 'hasgeek'}, {'member_name': 'kiran', 'organization_name': 'pycon'}] 

EVENTS = [{'created_by': 1, 'title': 'fiftheelephant', 'name': 'fifthelephant2012'}]

EVENTS_DETAILS = [{'name': 'fifthelephant2012', 'main_event_start_date': datetime.datetime.utcnow(), 'main_event_end_date': datetime.timedelta(days(1)) + datetime.utcnow(), 'hacknight_start_date': datetime.datetime.utcnow() - datetime.timedelate(days=15), 'main_event_end_date': datetime.datetime.utcnow() - datetime.timedelta(days=15) + datetime.timedelta(days(hours=10)), 'main_event_website': 'http://fifthelephant.com'}]

EVENTS_LOCATION = [{'name': 'fifthelephant2012', 'location': 'Bangalore', 'country': 'India'}]

