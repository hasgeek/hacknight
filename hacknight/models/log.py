# -*- coding: utf-8 -*-

import datetime

from hacknight.models import db, BaseMixin, User, Event

__all__ = ['PaymentGatewayLog', 'TRANSACTION_STATUS', 'transaction_status']


class TRANSACTION_STATUS:
    PENDING = 0
    FAILURE = 1
    SUCCESS = 2


transaction_status = {
    u'success': TRANSACTION_STATUS.SUCCESS,
    u'pending': TRANSACTION_STATUS.PENDING,
    u'failure': TRANSACTION_STATUS.FAILURE,
}


class PaymentGatewayLog(BaseMixin, db.Model):
    __tablename__ = "payment_gateway_log"

    user_id = db.Column(None, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)

    event_id = db.Column(None, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event, backref=db.backref('payment_gateway_logs'))

    status = db.Column(db.Integer, default=TRANSACTION_STATUS.PENDING, nullable=False)
    order_no = db.Column(db.Unicode(20), nullable=False)

    server_response = db.Column(db.UnicodeText(), nullable=True)
    start_datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    end_datetime = db.Column(db.DateTime, nullable=True)

    @classmethod
    def get_recent_transaction(cls, user):
        return cls.query.filter_by(user=user).order_by(PaymentGatewayLog.id.desc()).first()
