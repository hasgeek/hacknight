# -*- coding: utf-8 -*-

import wtforms

__all__ = ['CommentForm', 'DeleteCommentForm', 'ConfirmDeleteForm']


class CommentForm(wtforms.Form):
    reply_to_id = wtforms.HiddenField('Parent', default="", id="comment_reply_to_id")
    edit_id = wtforms.HiddenField('Edit', default="", id="comment_edit_id")
    message = wtforms.TextAreaField('Add comment', id="comment_message", validators=[wtforms.validators.Required()])


class DeleteCommentForm(wtforms.Form):
    comment_id = wtforms.HiddenField('Comment', validators=[wtforms.validators.Required()])


class ConfirmDeleteForm(wtforms.Form):
    """
    Confirm a delete operation
    """
    # The labels on these widgets are not used. See delete.html.
    delete = wtforms.SubmitField(u"Delete")
    cancel = wtforms.SubmitField(u"Cancel")
