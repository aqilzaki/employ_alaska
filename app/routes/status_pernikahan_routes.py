from flask import Blueprint
from app.controllers.status_pernikahan_controller import StatusPernikahanController

status_pernikahan_bp = Blueprint('status_pernikahan', __name__)

# GET /api/status-pernikahan
status_pernikahan_bp.route('/', methods=['GET'])(StatusPernikahanController.get_all)

# GET /api/status-pernikahan/<id>
status_pernikahan_bp.route('/<string:id>', methods=['GET'])(StatusPernikahanController.get_by_id)

# POST /api/status-pernikahan
status_pernikahan_bp.route('/', methods=['POST'])(StatusPernikahanController.create)

# PUT /api/status-pernikahan/<id>
status_pernikahan_bp.route('/<string:id>', methods=['PUT'])(StatusPernikahanController.update)

# DELETE /api/status-pernikahan/<id>
status_pernikahan_bp.route('/<string:id>', methods=['DELETE'])(StatusPernikahanController.delete)
