from flask import g
from flask_httpauth import HTTPBasicAuth
from plivo.sms.models.account import Account


auth = HTTPBasicAuth()

# Multiple stragegies can be applied here depending on requirements
# Each user can be fetched from database and cached locally for a specific period of time in some kind of local cache
# For the premise of this project, we have very few accounts,
# so we are caching all the accounts permanently on the server
accounts = {account.username: account.__dict__ for account in Account.query.all()}


@auth.get_password
def get_pw(username):
    account = accounts.get(username, {})
    if account:
        g.account = account
    return account.get('auth_id')
