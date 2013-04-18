# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField
from baseframe.staticdata import country_codes

__all__ = ['VenueForm']


class VenueForm(Form):
    title = wtf.TextField("Name", description="Name of the venue", validators=[wtf.Required(), wtf.validators.length(max=250)])
    description = RichTextField("Notes", description="Notes about the venue",
        content_css="/static/css/editor.css")
    address1 = wtf.TextField("Address (line 1)", validators=[wtf.Required(), wtf.validators.length(max=80)])
    address2 = wtf.TextField("Address (line 2)", validators=[wtf.Optional(), wtf.validators.length(max=80)])
    city = wtf.TextField("City", validators=[wtf.Required(), wtf.validators.length(max=30)])
    state = wtf.TextField("State", validators=[wtf.Optional(), wtf.validators.length(max=30)])
    postcode = wtf.TextField("Post code", validators=[wtf.Optional(), wtf.validators.length(max=20)])
    country = wtf.SelectField("Country", validators=[wtf.Required(), wtf.validators.length(max=2)], choices=country_codes, default="IN")
    latitude = wtf.DecimalField("Latitude", places=None, validators=[wtf.Optional(), wtf.NumberRange(-90, 90)])
    longitude = wtf.DecimalField("Longitude", places=None, validators=[wtf.Optional(), wtf.NumberRange(-180, 180)])
    profile_id = wtf.SelectField("Owner", description="The owner of this listing", coerce=int, validators=[wtf.Required()])


class FourSquareVenueSearchForm(Form):
    name = wtf.TextField("Name", validators=[wtf.Required(), wtf.validators.length(max=100)], description="Name of the venue like HasGeek")
    city =wtf.TextField("City", validators=[wtf.Required(), wtf.validators.length(max=80)], description="Name of the city like Bangalore")


class FourSquareVenueAddForm(FourSquareVenueSearchForm):
    venues = wtf.SelectMultipleField("Select Venue to Add", coerce=int, description="You can select more than one venue from drop down list")
