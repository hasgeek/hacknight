# -*- coding: utf-8 -*-

from flask import render_template, url_for, flash, abort, g
from coaster.views import load_model
from baseframe.forms import render_redirect, render_form, render_delete_sqla

from hacknight import app
from hacknight.models import db, Venue
from hacknight.forms.venue import VenueForm
from hacknight.views.login import lastuser


@app.route('/venue')
def venue_list():
    venues = Venue.query.order_by('title').all()
    return render_template('venuelist.html', venues=venues)


@app.route('/venue/<venue>')
@load_model(Venue, {'name': 'venue'}, 'venue')
def venue_view(venue):
    return render_template('venue.html', venue=venue)


@app.route('/venue/new', methods=['GET', 'POST'])
@lastuser.requires_login
def venue_new():
    form = VenueForm()
    form.profile_id.choices = [(p.id, p.title) for p in g.user.profiles]
    if form.validate_on_submit():
        venue = Venue()
        form.populate_obj(venue)
        venue.make_name()
        db.session.add(venue)
        db.session.commit()
        flash(u"You have created a new venue", "success")
        return render_redirect(venue.url_for(), code=303)
    return render_form(form=form, title="New Venue", submit=u"Create", cancel_url=venue.url_for(), ajax=False)


@app.route('/venue/<venue>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Venue, {'name': 'venue'}, 'venue')
def venue_edit(venue):
    if not (lastuser.has_permission('siteadmin') or venue.profile.userid in g.user.user_organizations_owned_ids()):
        abort(403)
    form = VenueForm(obj=venue)
    form.profile_id.choices = [(p.id, p.title) for p in g.user.profiles]
    form.profile_id.choices.insert(0, (venue.profile.id, venue.profile.title))
    if form.validate_on_submit():
        form.populate_obj(venue)
        venue.make_name()
        db.session.commit()
        flash(u"You have edited details for venue %s" % venue.title, "success")
        return render_redirect(url_for('venue_view', venue=venue.name), code=303)
    return render_form(form=form, title="Edit Venue", submit=u"Save",
        cancel_url=url_for('venue_view', venue=venue.name), ajax=False)


@app.route('/venue/<venue>/delete', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Venue, {'name': 'venue'}, 'venue')
def venue_delete(venue):
    if not lastuser.has_permission('siteadmin') and venue.profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)
    return render_delete_sqla(venue, db, title=u"Confirm delete",
        message=u"Delete venue '%s'? This cannot be undone." % venue.title,
        success=u"You have deleted playlist '%s'." % venue.title,
        next=url_for('venue_list'))
