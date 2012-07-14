# -*- coding: utf-8 -*-
from hacknight.models.event import PROFILE_TYPE, EVENT_STATUS
import datetime

now = datetime.datetime.now()
USERS = [{'userid': u'kRxvoscJQg6kCE3FWErj_w', 'username': u'kracekumar', 'fullname': u'kracekumar', 'lastuser_token': u'Qfy22E2RSsyrym6DT8NcQw', 'lastuser_token_type': u'bearer', 'lastuser_token_scope': u'organizations id', 'userinfo': {"username": "kracekumar", "organizations": {"owner": [{"userid": "7ZAJMXDHT4ayE9yN8Fqqzw", "name": "pycon", "title": "pycon"}, {"userid": "EkDqDfW6SqOZxu5KYKZqfw", "name": "hasgeek", "title": "Hasgeek"}], "member": [{"userid": "7ZAJMXDHT4ayE9yN8Fqqzw", "name": "pycon", "title": "pycon"}, {"userid": "EkDqDfW6SqOZxu5KYKZqfw", "name": "hasgeek", "title": "Hasgeek"}]}, "fullname": "kracekumar", "userid": "kRxvoscJQg6kCE3FWErj_w", "teams": [{"org": "EkDqDfW6SqOZxu5KYKZqfw", "userid": "xDDIgGbKSl-doTzna5MnBA", "title": "Owners"}, {"org": "EkDqDfW6SqOZxu5KYKZqfw", "userid": "4wEMkG7JRMydWKG-ZI361g", "title": "hackers"}, {"org": "7ZAJMXDHT4ayE9yN8Fqqzw", "userid": "9D3_SX5MRgqpFsZFYJqDSA", "title": "Owners"}, {"org": "7ZAJMXDHT4ayE9yN8Fqqzw", "userid": "8M_bkHq8RFemUrpwqfOmcw", "title": "python hackers"}]}}]
PROFILES = [{'userid': u'kRxvoscJQg6kCE3FWErj_w', 'description': u'User kracekumar', 'name': u'kracekumar', 'title': u'kracekumar', 'type': PROFILE_TYPE.PERSON}]
VENUES = [{'description': u'Center for Internet Society', 'address1': u'No 194, 2nd C Cross, 4th Main Opp. Domlur Club, Domlur 2nd Stage, Bangalore, Karnataka – 560 071',\
            'city': u'bangalore', 'state': u'India', 'postcode': u'560071', 'website': 'http://cis-india.org/', 'name': u'CIS', 'title': u'CIS - Bangalore'}]
EVENTS = [{'description': u"""The data hacknight is open to enthusiasts, geeks, designers, mathematicians and statisticians. It is an occasion to work on a data project that you have always wanted to,
be it:

    Finding patterns in datasets and coming up with interesting analytical models.
    Working on visualization challenges - how you would like to represent your data.
    Working with a new tool, such as R, Excel, Pig, Hive, or even Hadoop.
    Building a cluster overnight, if you have set your eyes on the sky!
    Scraping data from sources and creating a repository.
    Other ideas that you may have!
    Or, take up one of our challenges and work with the datasets!

Propose your project ideas here, form teams, and hack your way to the glory of geekness!

If you have datasets that you would like to share with others, create a proposal out of it by giving more information about the dataset, links or pointers so that  others can come up with ideas.

This hacknight is part of a larger conference on big data, analytics and cross-industry applications called The Fifth Elephant. The Fifth Elephant takes place on 27 and 28 July, 2012, at the Nimhans Convention Centre in Bangalore. The hacknight is free if you have purchased your ticket to the event. If not, the entry fee is Rs. 500.

HasGeek will provide you with food, beverages and a cool hacknight t-shirt during the 16 hours of hacking!""", 'website': u'http://fifthelephant.in/2012', 'status': EVENT_STATUS.PUBLISHED, 'ticket_price': 500,\
'name': u'fifthelephant Bangalore Hacknight', 'title': u'Data Hacknight Bangalore', 'start_datetime': now, 'end_datetime': now + datetime.timedelta(hours=16)}]
PARTICIPANTS = [{'reason_to_join': u'Curiosity', 'email': u'kracekumar@hasgeek.in', 'phone_no': u'+91-85530-29521', 'job_title': u'Software Engineer', 'company': u'HasGeek', 'status': 2}]
PROJECTS = [{'url_id': u'twitter_mining', 'name': u'Twitter Minner', 'title': u'Twitter Mining', 'description': u'Twitter is assest of the decade, mine to become rich, Find patterns, trends, what people tweet',\
              'blurb': u'Twitter is assest of the decade, mine to become rich, Find patterns, trends, what people tweet', }]
SPONSORS = [{'name': 'neo4j', 'description': 'World Leading graph database', 'image_url': 'http://fifthelephant.in/_themes/fifthelephant/img/2012/sponsors/neo4j-logo-hacknight.png', 'title': 'neo4j', 'title': 'neo4j - Test'}]
