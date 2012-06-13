# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField, DateTimeInput

__all__ = ['EventForm']

class EventForm(Form):
    title = wtf.TextField("Title", description="Name of the Event", validators=[wtf.Required(), wtf.NoneOf(values=["New"])])
    description = RichTextField("Description", description="Description of the project")
    #need to datepicker here, for time being while python datetime module is used inside views
    start_datetime = wtf.DateTimeField("Start Date and Time", widget=DateTimeInput(), description="Hacknight Start DateTime", validators=[wtf.Required()])
    end_datetime = wtf.DateTimeField("End Date and Time", widget=DateTimeInput(), description="Hacknight End DateTime", validators=[wtf.Required()])
    ticket_price = wtf.TextField("Ticket Price", description="Entry fee, if any, to be paid at the venue.")
    total_participants = wtf.IntegerField("Total Participants", description="Total Participants for Hacknight. E.g: 50", default=50, validators=[wtf.Required()])
    website = wtf.TextField("Website",description="Related Website (Optional)", validators=[wtf.Optional()])

    def validate_end_datetime(self, field):
        if field.data < self.start_datetime.data:
            raise wtf.ValidationError(u"Your event can’t end before it starts.")

class EventManagerForm(Form):
    def make_participants(self, participants):
        participants = wtf.SelectMultipleField("Select participant to confirm", description="Select participant to confirm")

