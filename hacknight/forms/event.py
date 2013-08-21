# -*- coding: utf-8 -*-

from flask import Markup
import wtforms
import wtforms.fields.html5
from wtforms.ext.sqlalchemy.fields import QuerySelectField
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
    title = wtforms.TextField("Title", description="Name of the Event", validators=[wtforms.validators.Required(), wtforms.validators.NoneOf(values=["new"]), wtforms.validators.length(max=250)])
    name = wtforms.TextField("URL name", validators=[wtforms.validators.Optional(), ValidName(),
        AvailableName(u"There’s another event with the same name", scoped=True), wtforms.validators.length(max=250)],
        description="URL identifier, leave blank to autogenerate")
    blurb = wtforms.TextField("Blurb", description="Single line blurb introducing the event", validators=[wtforms.validators.length(max=250)])
    description = RichTextField("Description", description="Detailed description of the event", linkify=False,
        content_css="/static/css/editor.css", tinymce_options = {
        "valid_elements": "p,br,strong/b,em/i,sup,sub,h3,h4,h5,h6,ul,ol,li,a[!href|title|target|class],blockquote,pre,code,img[!src|alt|class|width|height|align]",
        "theme_advanced_buttons1": "bold,italic,|,sup,sub,|,bullist,numlist,|,link,unlink,|,blockquote,|,removeformat,code,image", "theme": "advanced"},
        sanitize_tags=['p', 'br', 'strong', 'em', 'sup', 'sub', 'h3', 'h4', 'h5', 'h6',
                'ul', 'ol', 'li', 'a', 'span', 'blockquote', 'pre', 'code', 'img',
                'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td', 'iframe'],
        sanitize_attributes={'a': ['href', 'title', 'target', 'class'],
                                'span': ['class'],
                                'img': ['src', 'alt', 'class', 'width', 'height', 'align']},
        )
    apply_instructions = RichTextField("Instructions for participants", description="This will be shown to participants on the hacknight joining form",
        content_css="/static/css/editor.css")
    venue = QuerySelectField("Venue",
        description=Markup('Venue for this event (<a href="/venue/new">make new</a>)'),
        query_factory=lambda: Venue.query, get_label='title',
        )
    start_datetime = DateTimeField("Start date/time", description="The date and time at which this event begins", validators=[wtforms.validators.Required()])
    end_datetime = DateTimeField("End date/time", description="The date and time at which this event ends", validators=[wtforms.validators.Required()])
    ticket_price = wtforms.TextField("Ticket price", description="Entry fee, if any, to be paid at the venue", validators=[wtforms.validators.length(max=250)])
    maximum_participants = wtforms.IntegerField("Venue capacity", description="The number of people this venue can accommodate.", default=50, validators=[wtforms.validators.Required()])
    website = wtforms.fields.html5.URLField("Website", description="Related Website (Optional)", validators=[wtforms.validators.Optional(), wtforms.validators.length(max=250), wtforms.validators.URL()])
    status = wtforms.SelectField("Event status", description="Current status of this hacknight", coerce=int, choices=STATUS_CHOICES)

    def validate_end_datetime(self, field):
        if field.data < self.start_datetime.data:
            raise wtforms.ValidationError(u"Your event can’t end before it starts.")


class EmailEventParticipantsForm(Form):
    pending_message = RichTextField("Pending Message", description="Message to be sent for pending participants. '*|FULLNAME|*' will be replaced with user's fullname.", validators=[wtforms.validators.Optional()], tinymce_options = {'convert_urls': False, 'remove_script_host': False})
    confirmation_message = RichTextField("Confirmation Message", description="Message to be sent for confirmed participants. '*|FULLNAME|*' will be replaced with user's fullname.", validators=[wtforms.validators.Optional()], tinymce_options = {'convert_urls': False, 'remove_script_host': False})
    rejected_message = RichTextField("Rejected Message", description="Message to be sent for rejected participants. '*|FULLNAME|*' will be replaced with user's fullname.", validators=[wtforms.validators.Optional()], tinymce_options = {'convert_urls': False, 'remove_script_host': False})
    waitlisted_message = RichTextField("Waitlisted Message", description="Message to be sent for waitlisted participants. '*|FULLNAME|*' will be replaced with user's fullname.", validators=[wtforms.validators.Optional()], tinymce_options = {'convert_urls': False, 'remove_script_host': False})


class ConfirmWithdrawForm(wtforms.Form):
    """
    Confirm a delete operation
    """
    delete = wtforms.SubmitField(u"Withdraw")
    cancel = wtforms.SubmitField(u"Cancel")


class SendEmailForm(Form):
    subject = wtforms.TextField("Subject", description="Subject for the email", validators=[wtforms.validators.Required(), wtforms.validators.length(max=250)])
    message = RichTextField("Message", description="Email message, only *|FULLNAME|* will be replaced with participant fullname", validators=[wtforms.validators.Required()], tinymce_options={'convert_urls': False, 'remove_script_host': False})
    send_to = wtforms.RadioField("Send email to", default=2, coerce=int)
