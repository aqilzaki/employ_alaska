from flask import Blueprint
from app.controllers.izin_controller import IzinController
izin_bp = Blueprint("izin", __name__)

izin_bp.route(
    "/ajukan",
    methods=["POST"]
)(IzinController.ajukan_izin)

izin_bp.route(
    "/update-status/<int:id>",
    methods=["PUT"]
)(IzinController.update_status)

izin_bp.route("/my-history", methods=["GET"])(IzinController.get_my_history_izin)


# note filter yang bisa digunakan
# ?status=APPROVED
# ?from=2025-01-01
# ?to=2025-01-31
# ?departemen=IT
