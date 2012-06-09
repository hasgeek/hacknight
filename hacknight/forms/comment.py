# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField

__all__ = ['CommentForm', 'DeleteCommentForm', 'ConfirmDeleteForm']


class CommentForm(wtf.Form):
    parent_id = wtf.HiddenField('Parent', default="", id="comment_parent_id")
    edit_id = wtf.HiddenField('Edit', default="", id="comment_edit_id")
    message = wtf.TextAreaField('Add comment', id="comment_message", validators=[wtf.Required()])



class DeleteCommentForm(wtf.Form):
    comment_id = wtf.HiddenField('Comment', validators=[wtf.Required()])


class ConfirmDeleteForm(wtf.Form):
    """
    Confirm a delete operation
    """
    # The labels on these widgets are not used. See delete.html.
    delete = wtf.SubmitField(u"Delete")
    cancel = wtf.SubmitField(u"Cancel")
