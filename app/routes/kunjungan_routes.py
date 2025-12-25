from flask import Blueprint
from app.controllers.kunjungan_controller import KunjunganController 
from app.controllers.report_kunjungan_controller import ReportKunjunganController
kunjungan_bp = Blueprint("kunjungan", __name__)

kunjungan_bp.route(
    "/kunjungan",
    methods=["POST"]
)(KunjunganController.submit_kunjungan)


kunjungan_report_bp = Blueprint("kunjungan_report", __name__)

kunjungan_report_bp.route(
    "/AE",
    methods=["GET"]
)(ReportKunjunganController.get_kunjungan)
