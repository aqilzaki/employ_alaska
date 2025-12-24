from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models.karyawan import Karyawan

def active_account_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()

        karyawan = Karyawan.query.get(identity)
        if not karyawan:
            return jsonify({
                "success": False,
                "message": "Akun tidak ditemukan"
            }), 404

        # asumsi kondisi akun AKTIF = "AKTIF"
        if karyawan.kondisi_akun.nama_kondisi_akun.lower() != "aktif":
            return jsonify({
                "success": False,
                "message": "Akun nonaktif / diblokir"
            }), 403

        return fn(*args, **kwargs)
    return wrapper
