# -*- coding: utf-8- *-

from hacknight.models import BaseMixin, BaseScopedIdNameMixin, BaseScopedIdMixin
from hacknight.models import db
from hacknight.models.event import Event
from hacknight.models.participant import Participant
from hacknight.models.user import User
from hacknight.models.vote import Vote, VoteSpace

__all__ = ['CommentSpace', 'Comment']

# What is this VoteSpace or CommentSpace attached to?
class SPACETYPE:
    PROPOSALSPACE = 0
    PROPOSALSPACESECTION = 1
    PROPOSAL = 2
    COMMENT = 3



class COMMENTSTATUS:
    PUBLIC = 0
    SCREENED = 1
    HIDDEN = 2
    SPAM = 3
    DELETED = 4  # For when there are children to be preserved


class CommentSpace(BaseMixin, db.Model):
    __tablename__ = 'commentspace'
    count = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, **kwargs):
        super(CommentSpace, self).__init__(**kwargs)
        self.count = 0


class Comment(BaseMixin, BaseScopedIdMixin, db.Model):
    __tablename__ = 'comment'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship(User, primaryjoin=user_id == User.id,
        backref=db.backref('comments', cascade="all"))
    commentspace_id = db.Column(db.Integer, db.ForeignKey('commentspace.id'), nullable=False)
    commentspace = db.relationship(CommentSpace, primaryjoin=commentspace_id == CommentSpace.id,
        backref=db.backref('comments', cascade="all, delete-orphan"))

    reply_to_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    children = db.relationship("Comment", backref=db.backref("reply_to", remote_side="Comment.id"))

    message = db.Column(db.Text, nullable=False)
    message_html = db.Column(db.Text, nullable=False)

    status = db.Column(db.Integer, default=0, nullable=False)

    votes_id = db.Column(db.Integer, db.ForeignKey('votespace.id'), nullable=False)
    votes = db.relationship(VoteSpace, uselist=False)

    edited_at = db.Column(db.DateTime, nullable=True)

    parent = db.synonym('commentspace')

    __table_args__ = (db.UniqueConstraint('url_id', 'commentspace_id'),)

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        self.votes = VoteSpace(type=SPACETYPE.COMMENT)

    def delete(self):
        """
        Delete this comment.
        """
        if len(self.children) > 0:
            self.status = COMMENTSTATUS.DELETED
            self.user = None
            self.message = ''
            self.message_html = ''
        else:
            if self.reply_to and self.reply_to.is_deleted:
                # If the parent comment is deleted, ask it to reconsider removing itself
                reply_to = self.reply_to
                reply_to.children.remove(self)
                db.session.delete(self)
                reply_to.delete()
            else:
                db.session.delete(self)

    @property
    def is_deleted(self):
        return self.status == COMMENTSTATUS.DELETED

    def sorted_children(self):
        return sorted(self.children, key=lambda child: child.votes.count)
