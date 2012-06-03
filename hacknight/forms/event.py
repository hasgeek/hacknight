# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField
#from baseframe.staticdata import timezones

__all__ = ['EventForm']


class EventForm(Form):
    title = wtf.TextField("Title", description="Name of the Event", validators=[wtf.Required()])
    description = RichTextField("Description", description="Description of the project")
    #need to datepicker here, for time being while python datetime module is used inside views
    start_datetime = wtf.DateTimeField("StartDateTime", description="Hacknight Start DateTime", validators=[wtf.Required()])
    end_datetime = wtf.DateTimeField("EndDateTime", description="Hacknight End DateTime", validators=[wtf.Required()])
    website = wtf.TextField("Main Event Website", validators=[wtf.Optional()])
