# -*- coding: utf-8- *-

from hacknight.models import BaseMixin, BaseScopedIdNameMixin
from hacknight.models import db
from hacknight.models.event import Event
from hacknight.models.participant import Participant

__all__ = ['CommentSpace', 'Comment']

class CommentSpace(db.Model, BaseMixin):
    __tablename__ = 'commentspace'
    type = db.Column(db.Integer, nullable=True)
    count = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, **kwargs):
        super(CommentSpace, self).__init__(**kwargs)
        self.count = 0


class Comment(db.Model, BaseMixin):
    __tablename__ = 'comment'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship(User, primaryjoin=user_id == User.id,
        backref=db.backref('comments', cascade="all"))
    commentspace_id = db.Column(db.Integer, db.ForeignKey('commentspace.id'), nullable=False)
    commentspace = db.relationship(CommentSpace, primaryjoin=commentspace_id == CommentSpace.id,
        backref=db.backref('comments', cascade="all, delete-orphan"))

    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    children = db.relationship("Comment", backref=db.backref("parent", remote_side="Comment.id"))

    message = db.Column(db.Text, nullable=False)
    message_html = db.Column(db.Text, nullable=False)

    status = db.Column(db.Integer, default=0, nullable=False)

    votes_id = db.Column(db.Integer, db.ForeignKey('votespace.id'), nullable=False)
    votes = db.relationship(VoteSpace, uselist=False)

    edited_at = db.Column(db.DateTime, nullable=True)

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
            if self.parent and self.parent.is_deleted:
                # If the parent is deleted, ask it to reconsider removing itself
                parent = self.parent
                parent.children.remove(self)
                db.session.delete(self)
                parent.delete()
            else:
                db.session.delete(self)

    @property
    def is_deleted(self):
        return self.status == COMMENTSTATUS.DELETED

    def sorted_children(self):
        return sorted(self.children, key=lambda child: child.votes.count)
