# -*- coding: utf-8 -*-

import wtforms
from flask_wtf import Form

__all__ = ['CommentForm', 'DeleteCommentForm', 'ConfirmDeleteForm']


class CommentForm(Form):
    reply_to_id = wtforms.HiddenField('Parent', default="", id="comment_reply_to_id")
    edit_id = wtforms.HiddenField('Edit', default="", id="comment_edit_id")
    message = wtforms.TextAreaField('Add comment', id="comment_message", validators=[wtforms.validators.Required()])


class DeleteCommentForm(Form):
    comment_id = wtforms.HiddenField('Comment', validators=[wtforms.validators.Required()])


class ConfirmDeleteForm(Form):
    """
    Confirm a delete operation
    """
    # The labels on these widgets are not used. See delete.html.
    delete = wtforms.SubmitField("Delete")
    cancel = wtforms.SubmitField("Cancel")
