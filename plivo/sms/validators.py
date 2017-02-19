from flask import g

from flask_inputs.inputs import Inputs
from flask_inputs.validators import JsonSchema

from plivo.sms.models.phone_number import PhoneNumber

sms_request_schema = {
    'type': 'object',
    'properties': {
        'to': {
            'type': 'string',
            'minLength': 6,
            'maxLength': 16
        },
        'from': {
            'type': 'string',
            'minLength': 6,
            'maxLength': 16
        },
        'text': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 120
        }
    },
    'required': ['to', 'from', 'text']
}


def validate_phone_number(phone_number):
    phone_numbers = PhoneNumber.query.filter_by(number=phone_number)
    valid_phone_account = filter(lambda phone_number_obj: phone_number_obj.account_id == g.account.get('id'),
                                 phone_numbers)
    if valid_phone_account:
        return True
    return False


class SmsRequestJsonValidator(Inputs):
    json = [JsonSchema(schema=sms_request_schema)]
