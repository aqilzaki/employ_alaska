from flask import Blueprint
from app.controllers.status_kerja_controller import StatusKerjaController

status_kerja_bp = Blueprint('status_kerja', __name__)

# GET /api/status-kerja - Get all status kerja
status_kerja_bp.route('/', methods=['GET'])(StatusKerjaController.get_all)

# GET /api/status-kerja/<id> - Get status kerja by ID
status_kerja_bp.route('/<string:id>', methods=['GET'])(StatusKerjaController.get_by_id)

# POST /api/status-kerja - Create new status kerja
status_kerja_bp.route('/', methods=['POST'])(StatusKerjaController.create)

# PUT /api/status-kerja/<id> - Update status kerja by ID
status_kerja_bp.route('/<string:id>', methods=['PUT'])(StatusKerjaController.update)

# DELETE /api/status-kerja/<id> - Delete status kerja by ID
status_kerja_bp.route('/<string:id>', methods=['DELETE'])(StatusKerjaController.delete)