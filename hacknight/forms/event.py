# -*- coding: utf-8 -*-

from flask import Markup
import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField, DateTimeField, ValidName, AvailableName
from hacknight.models import Venue, EVENT_STATUS

__all__ = ['EventForm', 'ConfirmWithdrawForm', 'SendEmailForm']


STATUS_CHOICES = [
    (EVENT_STATUS.DRAFT, 'Draft'),
    (EVENT_STATUS.PUBLISHED, 'Published'),
    (EVENT_STATUS.ACTIVE, 'Active'),
    (EVENT_STATUS.COMPLETED, 'Completed'),
    (EVENT_STATUS.CANCELLED, 'Cancelled'),
    (EVENT_STATUS.CLOSED, 'Closed'),
    (EVENT_STATUS.REJECTED, 'Rejected'),
    (EVENT_STATUS.WITHDRAWN, 'Withdrawn')
]


class EventForm(Form):
    title = wtf.TextField("Title", description="Name of the Event", validators=[wtf.Required(), wtf.NoneOf(values=["new"]), wtf.validators.length(max=250)])
    name = wtf.TextField("URL name", validators=[wtf.Optional(), ValidName(),
            AvailableName(u"There’s another event with the same name", scoped=True), wtf.validators.length(max=250)],
        description="URL identifier, leave blank to autogenerate")
    blurb = wtf.TextField("Blurb", description="Single line blurb introducing the event", validators=[wtf.validators.length(max=250)])
    description = RichTextField("Description", description="Detailed description of the event",
        content_css="/static/css/editor.css")
    apply_instructions = RichTextField("Instructions for participants", description="This will be shown to participants on the hacknight joining form",
        content_css="/static/css/editor.css")
    venue = wtf.QuerySelectField("Venue",
        description=Markup('Venue for this event (<a href="/venue/new">make new</a>)'),
        query_factory=lambda: Venue.query, get_label='title',
        )
    start_datetime = DateTimeField("Start date/time", description="The date and time at which this event begins", validators=[wtf.Required()])
    end_datetime = DateTimeField("End date/time", description="The date and time at which this event ends", validators=[wtf.Required()])
    ticket_price = wtf.TextField("Ticket price", description="Entry fee, if any, to be paid at the venue", validators=[wtf.validators.length(max=250)])
    total_participants = wtf.IntegerField("Venue capacity", description="The number of people this venue can accommodate. Registrations will be closed after that. Use 0 to indicate unlimited capacity", default=50, validators=[wtf.Required()])
    website = wtf.html5.URLField("Website", description="Related Website (Optional)", validators=[wtf.Optional(), wtf.validators.length(max=250), wtf.URL()])
    status = wtf.SelectField("Event status", description="Current status of this hacknight", coerce=int, choices=STATUS_CHOICES)

    def validate_end_datetime(self, field):
        if field.data < self.start_datetime.data:
            raise wtf.ValidationError(u"Your event can’t end before it starts.")


class EmailEventParticipantsForm(Form):
    pending_message = RichTextField("Pending Message", description="Message to be sent for pending participants. '*|FULLNAME|*' will be replaced with user's fullname.", validators=[wtf.Optional()], tinymce_options = {'convert_urls': False, 'remove_script_host': False})
    confirmation_message = RichTextField("Confirmation Message", description="Message to be sent for confirmed participants. '*|FULLNAME|*' will be replaced with user's fullname.", validators=[wtf.Optional()], tinymce_options = {'convert_urls': False, 'remove_script_host': False})
    rejected_message = RichTextField("Rejected Message", description="Message to be sent for rejected participants. '*|FULLNAME|*' will be replaced with user's fullname.", validators=[wtf.Optional()], tinymce_options = {'convert_urls': False, 'remove_script_host': False})
    waitlisted_message = RichTextField("Waitlisted Message", description="Message to be sent for waitlisted participants. '*|FULLNAME|*' will be replaced with user's fullname.", validators=[wtf.Optional()], tinymce_options = {'convert_urls': False, 'remove_script_host': False})


class ConfirmWithdrawForm(wtf.Form):
    """
    Confirm a delete operation
    """
    delete = wtf.SubmitField(u"Withdraw")
    cancel = wtf.SubmitField(u"Cancel")


class SendEmailForm(Form):
    subject = wtf.TextField("Subject", description="Subject for the email", validators=[wtf.Required(), wtf.validators.length(max=250)])
    message = RichTextField("Message", description="Email message, only `FULLNAME` will be replaced with participant fullname", validators=[wtf.Required()])
    send_to = wtf.RadioField("Send email to", default=2, coerce=int)
