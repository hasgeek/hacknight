# -*- coding: utf-8 -*-

from flask import render_template, g, abort, flash
from coaster.views import load_model
from baseframe.forms import render_redirect, render_form
from hacknight import app
from hacknight.models import db, Profile, User, Event
from hacknight.models.event import profile_types, Event
from hacknight.forms.profile import ProfileForm
from hacknight.views.login import lastuser
from hacknight.models.participant import Participant
from datetime import datetime
from pytz import utc


@app.route('/<profile>')
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_view(profile):
    events = Event.query.filter_by(profile_id=profile.id).all()
    upcoming_events = Event.query.filter_by(profile_id=profile.id).filter(Event.end_datetime > datetime.utcnow()).order_by(Event.start_datetime.asc()).all()
    past_events = Event.query.filter_by(profile_id=profile.id).filter(Event.end_datetime < datetime.utcnow()).order_by(Event.end_datetime.desc()).all() 
    user = User.query.filter_by(userid=profile.userid).first()
    return render_template('profile.html', profile=profile, events=events, upcoming_events=upcoming_events, past_events=past_events, is_user=True if user else False)


@app.route('/<profile>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_edit(profile):
    if profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)
    form = ProfileForm(obj=profile)
    # FIXME: The way "choices" are populated is very confusing. Make this clearer.
    if profile.userid == g.user.userid:
        form.type.choices = [(1, profile_types[1])]
    else:
        choices = profile_types.items()
        choices.sort()
        choices.pop(0)
        choices.pop(0)
        form.type.choices = choices
    if form.validate_on_submit():
        form.populate_obj(profile)
        db.session.commit()
        flash(u"Edited description for profile", 'success')
        return render_redirect(profile.url_for(), code=303)
    return render_form(form=form, title=u"Edit profile", submit=u"Save",
        cancel_url=profile.url_for(), ajax=True)
