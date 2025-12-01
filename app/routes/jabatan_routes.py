from flask import Blueprint
from app.controllers.jabatan_controller import JabatanController

jabatan_bp = Blueprint('jabatan', __name__)

# GET /api/jabatan - Get all jabatan
jabatan_bp.route('/', methods=['GET'])(JabatanController.get_all)

# GET /api/jabatan/<id> - Get jabatan by ID
jabatan_bp.route('/<string:id>', methods=['GET'])(JabatanController.get_by_id)

# POST /api/jabatan - Create new jabatan
jabatan_bp.route('/', methods=['POST'])(JabatanController.create)

# PUT /api/jabatan/<id> - Update jabatan by ID
jabatan_bp.route('/<string:id>', methods=['PUT'])(JabatanController.update)

# DELETE /api/jabatan/<id> - Delete jabatan by ID
jabatan_bp.route('/<string:id>', methods=['DELETE'])(JabatanController.delete)