from flask import Blueprint
from app.controllers.report_absensi_controller import ReportAbsensiController

report_absensi_bp = Blueprint("report_absensi", __name__)

report_absensi_bp.route(
    "/report",
    methods=["GET"]
)(ReportAbsensiController.report_absensi)

report_absensi_bp.route(
    "/report/me",
    methods=["GET"]
)(ReportAbsensiController.get_my_absensi)