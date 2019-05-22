# -*- coding: utf-8 -*-

import wtforms
from coaster.utils import sorted_timezones
from baseframe.forms import Form, RichTextField

__all__ = ['VenueForm']


class VenueForm(Form):
    title = wtforms.TextField("Name", description="Name of the venue", validators=[wtforms.validators.Required(), wtforms.validators.length(max=250)])
    description = RichTextField("Notes", description="Notes about the venue",
        content_css="/static/css/editor.css")
    address1 = wtforms.TextField("Address (line 1)", validators=[wtforms.validators.Required(), wtforms.validators.length(max=80)])
    address2 = wtforms.TextField("Address (line 2)", validators=[wtforms.validators.Optional(), wtforms.validators.length(max=80)])
    city = wtforms.TextField("City", validators=[wtforms.validators.Required(), wtforms.validators.length(max=30)])
    state = wtforms.TextField("State", validators=[wtforms.validators.Optional(), wtforms.validators.length(max=30)])
    postcode = wtforms.TextField("Post code", validators=[wtforms.validators.Optional(), wtforms.validators.length(max=20)])
    country = wtforms.SelectField("Country", validators=[wtforms.validators.Required(), wtforms.validators.length(max=2)], choices=country_codes, default="IN")
    timezone = wtforms.SelectField('Timezone', validators=[wtforms.validators.Required()], choices=sorted_timezones())
    latitude = wtforms.DecimalField("Latitude", places=None, validators=[wtforms.validators.Optional(), wtforms.validators.NumberRange(-90, 90)])
    longitude = wtforms.DecimalField("Longitude", places=None, validators=[wtforms.validators.Optional(), wtforms.validators.NumberRange(-180, 180)])
    profile_id = wtforms.SelectField("Owner", description="The owner of this listing", coerce=int, validators=[wtforms.validators.Required()])
