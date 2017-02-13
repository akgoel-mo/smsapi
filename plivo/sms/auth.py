from flask_httpauth import HTTPBasicAuth
from plivo.sms.models.account import Account


auth = HTTPBasicAuth()

# Multiple stragegies can be applied here depending on requirements
# Each user can be fetched from database and cached locally for a specific period of time in some kind of local cache
# For the premise of this project, we have very few users, so we are caching all the users permanently on the server
users = {account.username: account.auth_id for account in Account.query.all()}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None
