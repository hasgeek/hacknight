# -*- coding: utf-8 -*-

import datetime

USERS = [{'userid': 'kRxvoscJQg6kCE3FWErj_w', 'username': 'kracekumar', 'fullname': 'kracekumar', 'lastuser_token': 'Qfy22E2RSsyrym6DT8NcQw', 'lastuser_token_type': 'bearer', 'lastuser_token_scope': 'organizations id', 'userinfo': {"username": "kracekumar", "organizations": {"owner": [{"userid": "7ZAJMXDHT4ayE9yN8Fqqzw", "name": "pycon", "title": "pycon"}, {"userid": "EkDqDfW6SqOZxu5KYKZqfw", "name": "hasgeek", "title": "Hasgeek"}], "member": [{"userid": "7ZAJMXDHT4ayE9yN8Fqqzw", "name": "pycon", "title": "pycon"}, {"userid": "EkDqDfW6SqOZxu5KYKZqfw", "name": "hasgeek", "title": "Hasgeek"}]}, "fullname": "kracekumar", "userid": "kRxvoscJQg6kCE3FWErj_w", "teams": [{"org": "EkDqDfW6SqOZxu5KYKZqfw", "userid": "xDDIgGbKSl-doTzna5MnBA", "title": "Owners"}, {"org": "EkDqDfW6SqOZxu5KYKZqfw", "userid": "4wEMkG7JRMydWKG-ZI361g", "title": "hackers"}, {"org": "7ZAJMXDHT4ayE9yN8Fqqzw", "userid": "9D3_SX5MRgqpFsZFYJqDSA", "title": "Owners"}, {"org": "7ZAJMXDHT4ayE9yN8Fqqzw", "userid": "8M_bkHq8RFemUrpwqfOmcw", "title": "python hackers"}]}}]

now = datetime.datetime.utcnow()

PROFILES = [{'userid': 'kRxvoscJQg6kCE3FWErj_w', 'description': 'An Premier Event Organization ', 'name': 'hasgeek.in', 'title': 'Hasgeek'}]

EVENTS = [{'userid': 'kRxvoscJQg6kCE3FWErj_w','title': 'fifthelephant2012', 'start_date': now, 'end_date': now + datetime.timedelta(0, 36000), 'website': 'http://fifthelephant.com', 'title': 'Data Lovers Meetup', 'name': '5el'}]

VENUES = [{'address': 'CIS, Domlur, Bangalore, India', 'description': 'All Internet work, hasgeek Office', 'title': 'Center For Internet society', 'name': 'http://hacknight.in/venue/cis/', 'latitude': 12.5, 'longitude': 77.8}]

PROJECTS = [{'title': 'Image Hijacker', 'description': 'this is my idea, I need more time to explain, but I am writing this because I want test to pass', 'event_name': '5el', 'name': 'Hack Bot'}]

PROJECT_MEMBERS = [{'fullname': 'kracekumar', 'project_title': 'Image Hijacker' }]


PARTICIPANTS = [{'fullname': 'kracekumar', 'event_name': '5el'}]

