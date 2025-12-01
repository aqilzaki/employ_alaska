from flask import Blueprint
from app.controllers.gaji_rule_controller import GajiRuleController

gaji_rule_bp = Blueprint('gaji_rule', __name__)

# GET all rules
gaji_rule_bp.route('/', methods=['GET'])(GajiRuleController.get_all)

# GET rule by ID
gaji_rule_bp.route('/<string:id>', methods=['GET'])(GajiRuleController.get_by_id)

# CREATE rule
gaji_rule_bp.route('/', methods=['POST'])(GajiRuleController.create)

# UPDATE rule
gaji_rule_bp.route('/<string:id>', methods=['PUT'])(GajiRuleController.update)

# DELETE rule
gaji_rule_bp.route('/<string:id>', methods=['DELETE'])(GajiRuleController.delete)
