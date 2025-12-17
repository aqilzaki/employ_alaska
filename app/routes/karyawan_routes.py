from flask import Blueprint
from app.controllers.karyawan_controller import KaryawanController

karyawan_bp = Blueprint('karyawan', __name__)

# GET /api/karyawan - Get all karyawan (with optional filters: ?jabatan=JB01&status=ST-KONT-001&search=john)
karyawan_bp.route('/', methods=['GET'])(KaryawanController.get_all)

# GET /api/karyawan/<id> - Get karyawan by ID
karyawan_bp.route('/<string:id>', methods=['GET'])(KaryawanController.get_by_id)

# POST /api/karyawan - Create new karyawan
karyawan_bp.route('/', methods=['POST'])(KaryawanController.create)

# PUT /api/karyawan/<id> - Update karyawan by ID
karyawan_bp.route('/<string:id>', methods=['PUT'])(KaryawanController.update)

# DELETE /api/karyawan/<id> - Delete karyawan by ID
karyawan_bp.route('/<string:id>', methods=['DELETE'])(KaryawanController.delete)

# PATCH /api/karyawan/update-kondisi-akun - Update kondisi akun of a karyawan
karyawan_bp.route('/update-kondisi-akun/<string:id_karyawan>', methods=['PATCH'])(KaryawanController.update_kondisi_akun_karyawan)

#patch /api/karyawan/update-kondisi-akun/<id_kondisi_akun> - Update kondisi akun of a karyawan
karyawan_bp.route('/get-all-karyawan-nonaktif-akun', methods=['GET'])(KaryawanController.get_all_karyawan_by_kondisi_non_aktif)