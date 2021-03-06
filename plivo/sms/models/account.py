from plivo.sms.models.phone_number import PhoneNumber
from plivo.sms.app import db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.String(20))
    username = db.Column(db.String(10))
    phone_numbers = db.relationship(PhoneNumber, backref='account', lazy='dynamic')

    def __init__(self, auth_id, username):
        self.auth_id = auth_id
        self.username = username

    def __repr__(self):
        return '<Account %r:%r>' % (self.username, self.auth_id)
