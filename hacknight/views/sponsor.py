# -*- coding: utf-8 -*-

from flask import render_template, g, abort, flash
from coaster.views import load_models
from baseframe.forms import render_form, render_redirect, render_delete_sqla
from hacknight import app
from hacknight.views.login import lastuser
from hacknight.models import db, Profile, Event, Sponsor
from hacknight.forms.sponsor import SponsorForm


@app.route('/<profile>/<event>/sponsors/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def sponsor_new(profile, event, form=None):
    if profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)

    form = SponsorForm()
    if form.validate_on_submit():
        sponsor = Sponsor(event=event)
        form.populate_obj(sponsor)
        sponsor.make_name()
        db.session.add(sponsor)
        db.session.commit()
        flash("Sponsor added")
        return render_redirect(event.url_for(), code=303)
    return render_form(form=form, title="New Sponsor", submit="Save",
        cancel_url=event.url_for(), ajax=False)


@app.route('/<profile>/<event>/sponsors/<sponsor>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Sponsor, {'name': 'sponsor', 'event': 'event'}, 'sponsor'),
    )
def sponsor_edit(profile, event, sponsor):
    if profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)

    else:
        form = SponsorForm(obj=sponsor)
        if form.validate_on_submit():
            form.populate_obj(sponsor)
            sponsor.make_name()
            db.session.commit()
            flash("Your changes have been saved", 'success')
            return render_redirect(sponsor.url_for(), code=303)
        return render_form(form=form, title="Edit sponsor", submit="Save",
            cancel_url=sponsor.url_for(), ajax=True)


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

    return render_delete_sqla(sponsor, db, title="Confirm delete",
        message="Delete Sponsor '%s'? This cannot be undone." % sponsor.title,
        success="You have deleted the sponsor '%s'." % sponsor.title,
         next=event.url_for())


@app.route('/<profile>/<event>/sponsors/<sponsor>/view', methods=['GET', 'POST'])
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Sponsor, {'name': 'sponsor', 'event': 'event'}, 'sponsor'),
    )
def sponsor_view(profile, event, sponsor):
    return render_template('sponsor.html.jinja2', sponsor=sponsor, profile=profile, event=event)
