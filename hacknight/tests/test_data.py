#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

USERS = [{'userid': 'kRxvoscJQg6kCE3FWErj_w', 'username': 'kracekumar', 'fullname': 'kracekumar', 'lastuser_token': 'Qfy22E2RSsyrym6DT8NcQw', 'lastuser_token_type': 'bearer', 'lastuser_token_scope': 'organizations id', 'userinfo': {"username": "kracekumar", "organizations": {"owner": [{"userid": "7ZAJMXDHT4ayE9yN8Fqqzw", "name": "pycon", "title": "pycon"}, {"userid": "EkDqDfW6SqOZxu5KYKZqfw", "name": "hasgeek", "title": "Hasgeek"}], "member": [{"userid": "7ZAJMXDHT4ayE9yN8Fqqzw", "name": "pycon", "title": "pycon"}, {"userid": "EkDqDfW6SqOZxu5KYKZqfw", "name": "hasgeek", "title": "Hasgeek"}]}, "fullname": "kracekumar", "userid": "kRxvoscJQg6kCE3FWErj_w", "teams": [{"org": "EkDqDfW6SqOZxu5KYKZqfw", "userid": "xDDIgGbKSl-doTzna5MnBA", "title": "Owners"}, {"org": "EkDqDfW6SqOZxu5KYKZqfw", "userid": "4wEMkG7JRMydWKG-ZI361g", "title": "hackers"}, {"org": "7ZAJMXDHT4ayE9yN8Fqqzw", "userid": "9D3_SX5MRgqpFsZFYJqDSA", "title": "Owners"}, {"org": "7ZAJMXDHT4ayE9yN8Fqqzw", "userid": "8M_bkHq8RFemUrpwqfOmcw", "title": "python hackers"}]}}]

now = datetime.datetime.utcnow()
EVENTS = [{'userid': 'kRxvoscJQg6kCE3FWErj_w', 'name': 'fifthelephant2012', 'hacknight_start_date': now, 'hacknight_end_date': now + datetime.timedelta(0, 36000), 'main_event_start_date': now + datetime.timedelta(15), 'main_event_end_date': now + datetime.timedelta(15, 36000 ), 'main_event_website': 'http://fifthelephant.com', 'title': 'Data Lovers Meetup'}]

LOCATIONS = [{'place': 'CIS, Domlur, Bangalore', 'country': 'India'}, {'place': 'Christ College, Bangalore', 'country': 'India'}]

EVENT_LOCATIONS = [{'name': 'fifthelephant2012', 'location': 'CIS, Domlur, Bangalore'}]

