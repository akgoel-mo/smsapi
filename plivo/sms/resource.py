from flask import Blueprint, jsonify, request, g
from plivo.sms.app import app
from plivo.sms.auth import auth
from plivo.sms.blocker.service import InboundMessageBlocker, OutboundMessageBlocker
from plivo.sms.rate_limiter.service import RateLimitService
from plivo.sms.validators import SmsRequestJsonValidator, validate_phone_number

sms_blueprint = Blueprint('sms_resource', __name__, url_prefix='/sms')


class SmsRequest(object):
    def __init__(self, sms_to=None, sms_from=None, sms_text=None, **kwargs):
        self.sms_to = sms_to or kwargs.get('to')
        self.sms_from = sms_from or kwargs.get('from')
        self.sms_text = sms_text or kwargs.get('text')


@sms_blueprint.before_request
def validate_request():
    request_validator = SmsRequestJsonValidator(request)
    if not request_validator.validate():
        app.logger.warning("JSON body failed validation: %r" % request.get_json())
        return jsonify(message="", error=request_validator.errors[0]), 400


@sms_blueprint.route('/inbound', methods=['POST'])
@auth.login_required
def inbound():
    request_json = request.get_json()
    sms_request = SmsRequest(**request_json)
    if not validate_phone_number(sms_request.sms_to):
        app.logger.warning("Invalid 'to' number - not found in phone numbers for account %s" % g.account.get('id'))
        return jsonify(message="", error='to parameter not found'), 400

    message_blocker = InboundMessageBlocker(sms_request)
    if message_blocker.needs_blocking():
        app.logger.warning("Blocking outbound messages for pair - from: {from}, to: {to}".format(**request_json))
        message_blocker.block_message()

    return jsonify(message="inbound sms ok", error="")


@sms_blueprint.route('/outbound', methods=['POST'])
@auth.login_required
def outbound():
    request_json = request.get_json()
    sms_request = SmsRequest(**request_json)
    if not validate_phone_number(sms_request.sms_from):
        return jsonify(message="", error='from parameter not found'), 400

    rate_limiter = RateLimitService(sms_request.sms_from)
    if rate_limiter.needs_blocking():
        app.logger.warning("Limit reached for from {from}".format(**request_json))
        return jsonify(message="", error='limit reached for from {from}'.format(**request_json)), 429

    message_blocker = OutboundMessageBlocker(sms_request)
    if message_blocker.needs_blocking():
        blocked = message_blocker.block_message()
        if blocked:
            app.logger.warning("Blocked outbound messages for pair - from: {from}, to: {to}".format(**request_json))
            return jsonify(message="", error='sms from {from} to {to} blocked by STOP request'.format(**request_json)), 422
    return jsonify(message="outbound sms ok", error="")
