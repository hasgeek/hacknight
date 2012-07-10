# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template, g, abort, flash, url_for, request, redirect
from coaster.views import load_models, jsonp
from baseframe.forms import render_form, render_redirect, ConfirmDeleteForm
from hacknight import app
from hacknight.views.login import lastuser
from hacknight.models import db, Profile, Event, Project, ProjectMember, Participant, User, Sponsor
from hacknight.forms.sponsor import SponsorForm


@app.route('/<profile>/<event>/sponsor/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    )
def sponsor_new(profile, event, form=None):
	if not profile:
		abort(404)

	if profile.userid not in g.user.user_organizations_owned_ids():
		abort(403)

	if not event:
		abort(404)

	form = SponsorForm()
	if form.validate_on_submit():
	    sponsor = Sponsor(event=event)
	    form.populate_obj(sponsor)
	    sponsor.make_name()
	    db.session.add(sponsor)
	    db.session.add(sponsor)
	    db.session.commit()
	    flash("Sponsor added")
	    return render_redirect(url_for('event_view', profile=profile.name, event=event.name), code=303)
	return render_form(form=form, title=u"New Sponsor", submit=u"Save",
	    cancel_url=url_for('event_view', profile=profile.name, event=event.name), ajax=False)


@app.route('/<profile>/<event>/sponsors/<sponsor>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Sponsor, {'name':'sponsor', 'event':'event'}, 'sponsor'),
    )
def sponsor_edit(profile, event, sponsor):
	if profile.userid not in g.user.user_organizations_owned_ids():
		abort(403)

	else:
	    form = SponsorForm(obj=sponsor)
	    if form.validate_on_submit():
	        form.populate_obj(sponsor)
	        db.session.commit()
	        flash(u"Your changes have been saved", 'success')
	        return render_redirect(url_for('sponsor_view', profile=profile.name, event=event.name,
	            sponsor=sponsor.name), code=303)
	    return render_form(form=form, title=u"Edit sponsor", submit=u"Save",
	        cancel_url=url_for('sponsor_view', profile=profile.name, event=event.name,
	            sponsor=sponsor.name), ajax=True)


@app.route('/<profile>/<event>/sponsors/<sponsor>/delete', methods=["GET", "POST"])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Sponsor, {'name':'sponsor', 'event':'event'}, 'sponsor'),
    )
def sponsor_delete(profile, event, sponsor):
    if not lastuser.has_permission('siteadmin') and profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)

    form = ConfirmDeleteForm()
    if form.validate_on_submit():
        if 'delete' in request.form:
            db.session.delete(sponsor)
            db.session.commit()
            flash("Sponsor removed", "success")
            return render_redirect(url_for('event_view', profile=profile.name, event=event.name), code=303)
    return render_template('baseframe/delete.html', form=form, title=u"Confirm delete",
        message=u"Delete '%s' ? " % (sponsor.title))


@app.route('/<profile>/<event>/sponsors/<sponsor>', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Sponsor, {'name':'sponsor', 'event':'event'}, 'sponsor'),
    )

def sponsor_view(profile, event, sponsor):
	if not profile:
		abort(404)

	if not event:
		abort(404)

	if not sponsor:
		abort(404)
	return render_template('sponsor.html', sponsor=sponsor)
