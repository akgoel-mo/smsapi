from plivo.sms.app import db


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16))
    account_id = db.Column(db.String(12), db.ForeignKey('account.id'))

    def __init__(self, number, account_id):
        self.number = number
        self.account_id = account_id

    def __repr__(self):
        return '<PhoneNumber %r:%r>' % (self.number, self.account_id)
