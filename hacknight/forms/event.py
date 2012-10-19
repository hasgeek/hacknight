# -*- coding: utf-8 -*-

from flask import Markup
import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField, DateTimeField, ValidName, AvailableName
from hacknight.models import Venue

__all__ = ['EventForm', 'ConfirmWithdrawForm']


class EventForm(Form):
    title = wtf.TextField("Title", description="Name of the Event", validators=[wtf.Required(), wtf.NoneOf(values=["new"]), wtf.validators.length(max=250)])
    name = wtf.TextField("URL name", validators=[wtf.Optional(), ValidName(),
            AvailableName(u"There’s another event with the same name", scoped=True), wtf.validators.length(max=250)],
        description="URL identifier, leave blank to autogenerate")
    blurb = wtf.TextField("Blurb", description="Single line blurb introducing the event", validators=[wtf.validators.length(max=250)])
    description = RichTextField("Description", description="Detailed description of the event",
        content_css="/static/css/editor.css")
    venue = wtf.QuerySelectField("Venue",
        description=Markup('Venue for this event (<a href="/venue/new">make new</a>)'),
        query_factory=lambda: Venue.query, get_label='title',
        )
    start_datetime = DateTimeField("Start date/time", description="The date and time at which this event begins", validators=[wtf.Required()])
    end_datetime = DateTimeField("End date/time", description="The date and time at which this event ends", validators=[wtf.Required()])
    ticket_price = wtf.TextField("Ticket price", description="Entry fee, if any, to be paid at the venue", validators=[wtf.validators.length(max=250)])
    total_participants = wtf.IntegerField("Venue capacity", description="The number of people this venue can accommodate. Registrations will be closed after that. Use 0 to indicate unlimited capacity", default=50, validators=[wtf.Required()])
    website = wtf.TextField("Website", description="Related Website (Optional)", validators=[wtf.Optional(), wtf.validators.length(max=250)])

    def validate_end_datetime(self, field):
        if field.data < self.start_datetime.data:
            raise wtf.ValidationError(u"Your event can’t end before it starts.")


class ConfirmWithdrawForm(wtf.Form):
    """
    Confirm a delete operation
    """
    delete = wtf.SubmitField(u"Withdraw")
    cancel = wtf.SubmitField(u"Cancel")
