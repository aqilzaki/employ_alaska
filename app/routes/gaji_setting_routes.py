from flask import Blueprint
from app.controllers.gaji_setting_controller import GajiSettingController

gaji_setting_bp = Blueprint("gaji_setting", __name__)

gaji_setting_bp.route("/", methods=["GET"])(GajiSettingController.get_all)
gaji_setting_bp.route("/<string:id>", methods=["GET"])(GajiSettingController.get_by_id)
gaji_setting_bp.route("/", methods=["POST"])(GajiSettingController.create)
gaji_setting_bp.route("/<string:id>", methods=["DELETE"])(GajiSettingController.delete)

# hitung gaji
gaji_setting_bp.route("/<string:id>/hitung", methods=["GET"])(GajiSettingController.hitung)
