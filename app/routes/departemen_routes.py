from flask import Blueprint
from app.controllers.departemen_controller import DepartemenController

departemen_bp = Blueprint('departemen', __name__)

# GET all departemen
departemen_bp.route('/', methods=['GET'])(DepartemenController.get_all)
# GET departemen by ID
departemen_bp.route('/<string:id>', methods=['GET'])(DepartemenController.get_by_id)
# CREATE departemen
departemen_bp.route('/', methods=['POST'])(DepartemenController.create)
# UPDATE departemen
departemen_bp.route('/<string:id>', methods=['PUT'])(DepartemenController.update)
# DELETE departemen
departemen_bp.route('/<string:id>', methods=['DELETE'])(DepartemenController.delete)
# Additional route to get employees by departemen ID
departemen_bp.route('/<string:id>/karyawan', methods=['GET'])(DepartemenController.get_karyawan_by_departemen)

