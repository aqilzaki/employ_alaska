from flask import Blueprint
from app.controllers.kondisi_akun_controller import KondisiAkunController

kondisi_akun_bp = Blueprint('kondisi_akun', __name__)

kondisi_akun_bp.route('/', methods=['GET'])(KondisiAkunController.get_all)
kondisi_akun_bp.route('/<string:id>', methods=['GET'])(KondisiAkunController.get_by_id)
kondisi_akun_bp.route('/', methods=['POST'])(KondisiAkunController.create)
kondisi_akun_bp.route('/<string:id>', methods=['PUT'])(KondisiAkunController.update)
kondisi_akun_bp.route('/<string:id>', methods=['DELETE'])(KondisiAkunController.delete)
