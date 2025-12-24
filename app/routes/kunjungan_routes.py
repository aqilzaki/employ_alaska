from flask import Blueprint
from app.controllers.kunjungan_controller import KunjunganController

kunjungan_bp = Blueprint("kunjungan", __name__)

kunjungan_bp.route(
    "/kunjungan",
    methods=["POST"]
)(KunjunganController.submit_kunjungan)
