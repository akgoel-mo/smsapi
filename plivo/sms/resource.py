from flask import Blueprint, jsonify
from plivo.sms.auth import auth

sms_blueprint = Blueprint('sms_resource', __name__, url_prefix='/sms')


@sms_blueprint.route('/inbound', methods=['POST'])
@auth.login_required
def inbound():
    return jsonify({"api": "inbound"})


@sms_blueprint.route('/outbound', methods=['POST'])
@auth.login_required
def outbound():
    return jsonify({"api": "outbound"})
