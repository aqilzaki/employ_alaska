from flask import Blueprint
from app.controllers.absensi_operator_controller import (
    AbsensiOperatorController
)

absensi_operator_bp = Blueprint("absensi_operator",__name__)

absensi_operator_bp.route("/in",methods=["POST"])(AbsensiOperatorController.absen_in)

absensi_operator_bp.route("/out",methods=["POST"])(AbsensiOperatorController.absen_out)
