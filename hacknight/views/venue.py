# -*- coding: utf-8 -*-

from flask import render_template, url_for, flash, abort, g, request, jsonify
from coaster.views import load_model
from baseframe.forms import render_redirect, render_form, render_delete_sqla

from hacknight import app, foursquare_client
from hacknight.models import db, Venue
from hacknight.forms.venue import VenueForm, FourSquareVenueSearchForm, FourSquareVenueAddForm
from hacknight.views.login import lastuser

#print app.config.keys()
#foursquare_client = foursquare.Foursquare(app.config['FOURSQUARE_CLIENT_ID'], app.config['FOURSQUARE_CLIENT_SECRET'])

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
    return render_form(form=form, title="New Venue", submit=u"Create", cancel_url=url_for('index'), ajax=False)


@app.route('/venue/foursquare/add', methods=['GET', 'POST'])
@lastuser.requires_login
def foursquare_search():
    form = FourSquareVenueSearchForm()
    add_form = FourSquareVenueAddForm()
    venues = []
    if form.validate_on_submit():
        name, city = form.name.data, form.city.data
        result = foursquare_client.venues.search(params={'query': name, 'near': city})
        #places = foursquare_client.venues.search(params={'query': name, 'near': city})
        if len(result['venues']) == 0:
            flash('Venue %s is not found in %s' % (name, city), 'error')
        else:
            venues.extend(venue for venue in result['venues'])
            add_form.venues.choices = [(index, venue['name']) for index, venue in enumerate(venues)]
            #raise
            if add_form.validate_on_submit() and add_form.venues.data:
                for index in add_form.venues.data:
                    venue = Venue()
                    venue.title = venues[index]['name']
                    venue.profile = g.user.profile
                    venue.description = venues[index]['location']['categories'] if 'shortName' in venues[index]['categories'] else ''
                    venue.address1 = venues[index]['location']['address'] if 'address' in venues[index]['location'] else ''
                    venue.address1 += ' ' + venues[index]['location']['crossStreet'] if 'crossStreet' in venues[index]['location'] else ''
                    venue.city = venues[index]['location']['city'] if 'city' in venues[index]['location'] else ''
                    venue.state = venues[index]['location']['state'] if 'state' in venues[index]['location'] else ''
                    venue.country = venues[index]['location']['cc'] if 'cc' in venues[index]['location'] else ''
                    venue.latitude = round(venues[index]['location']['lat'], 8) if 'lat' in venues[index]['location'] else None
                    venue.longitude = round(venues[index]['location']['lng'], 8) if 'lng' in venues[index]['location'] else None
                    venue.postcode = venues[index]['location']['postalCode'] if 'postalCode' in venues[index]['location'] else ''
                    venue.make_name()
                    db.session.add(venue)
                    db.session.commit()
                return render_redirect(url_for('venue_list'), code=303)
            else:
                return render_form(form=add_form, title="Add FourSquare Place",
                    submit="Add", cancel_url=url_for('foursquare_search'), ajax=False)
    return render_form(form=form, title="Search venue in FourSquare",
        submit=u"Search", cancel_url=url_for('index'), ajax=False)


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
