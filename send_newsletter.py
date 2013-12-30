#! /usr/bin/env python

import datetime
import sys
import logging

from jinja2 import Environment, PackageLoader, TemplateNotFound
from html2text import html2text

from hacknight import app, init_for
from hacknight.models import EmailCampaign, EmailCampaignUser, EMAIL_CAMPAIGN_STATUS, Event, User, db
from hacknight.views.event import send_email


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('send_newsletter')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('send_newsletter.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

# Jinja2 template for newsletter

env = Environment(loader=PackageLoader('hacknight', 'templates'))


def get_template(name='send_newsletter.html'):
    try:
        template = env.get_template(name)
        return template
    except TemplateNotFound, e:
        logger.error(e)
        return None


def send_emails(event, email_campaign):
    sender = User.query.filter_by(userid=event.profile.userid).first()
    # We need request context to generate event url.
    ctx = app.test_request_context('/')
    ctx.push()
    count = 0
    for user in email_campaign.yet_to_send():
        if user.send_newsletter and user.email and user.email != sender.email:
            subject = u"New Hacknight {0}".format(event.title)
            template = get_template()
            html = template.render(user=user, event=event)
            if html:
                text = html2text(html)
                send_email(sender=(sender.fullname, sender.email), to=user.email,
                    subject=subject, body=text, html=html)
                email_campaign_user = EmailCampaignUser(user=user, email_campaign=email_campaign)
                db.session.add(email_campaign_user)
                db.session.commit()
                count += 1
            else:
                logger.info(u"Unable to load template.")
                break
    logger.info(u"Email campaign completed for {0} users.".format(count))


def main():
    try:
        future_events = Event.upcoming_events()
        for event in future_events:
            if not EmailCampaign.sent_for(event):
                start_datetime = datetime.datetime.now()
                name = u'-'.join(["Newsletter campaign", event.title])
                email_campaign = EmailCampaign.get(event)
                if not email_campaign:
                    email_campaign = EmailCampaign(name=name, title=name, start_datetime=start_datetime, event=event)
                    db.session.add(email_campaign)
                    db.session.commit()
                send_emails(event, email_campaign)
                email_campaign.end_datetime = datetime.datetime.now()
                email_campaign.status = EMAIL_CAMPAIGN_STATUS.COMPLETED
                db.session.commit()
    except Exception, e:
        logger.exception(e)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        init_for(sys.argv[1])
        main()
    else:
        print("Missing parameter")
        print("python send_newsletter.py [development|production]")
