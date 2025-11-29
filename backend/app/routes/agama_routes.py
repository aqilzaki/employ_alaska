from flask import Blueprint
from app.controllers.agama_controller import AgamaController
agama_bp = Blueprint('agama', __name__)
# GET /api/agama - Get all agama
agama_bp.route('/', methods=['GET'])(AgamaController.get_all)
# GET /api/agama/<id> - Get agama by ID
agama_bp.route('/<string:id>', methods=['GET'])(AgamaController.get_by_id)
# POST /api/agama - Create new agama
agama_bp.route('/', methods=['POST'])(AgamaController.create)
# PUT /api/agama/<id> - Update agama by ID
agama_bp.route('/<string:id>', methods=['PUT'])(AgamaController.update)
# DELETE /api/agama/<id> - Delete agama by ID
agama_bp.route('/<string:id>', methods=['DELETE'])(AgamaController.delete)
