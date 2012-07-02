# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField
from baseframe.staticdata import country_codes

__all__ = ['VenueForm']


class VenueForm(Form):
    title = wtf.TextField("Name", description="Name of the venue", validators=[wtf.Required()])
    description = RichTextField("Notes", description="Notes about the venue",
        content_css="/static/css/editor.css")
    address1 = wtf.TextField("Address (line 1)", validators=[wtf.Required()])
    address2 = wtf.TextField("Address (line 2)", validators=[wtf.Optional()])
    city = wtf.TextField("City", validators=[wtf.Required()])
    state = wtf.TextField("State", validators=[wtf.Optional()])
    postcode = wtf.TextField("Post code", validators=[wtf.Optional()])
    country = wtf.SelectField("Country", validators=[wtf.Required()], choices=country_codes, default="IN")
    latitude = wtf.DecimalField("Latitude", places=None, validators=[wtf.Optional(), wtf.NumberRange(-90, 90)])
    longitude = wtf.DecimalField("Longitude", places=None, validators=[wtf.Optional(), wtf.NumberRange(-180, 180)])
    profile_id = wtf.SelectField("Owner", description="The owner of this listing", coerce=int, validators=[wtf.Required()])
