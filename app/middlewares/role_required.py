from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models.karyawan import Karyawan

def role_required(
    jabatan: list[str] = None,
    departemen: list[str] = None
):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            karyawan = Karyawan.query.get(identity)

            if not karyawan:
                return jsonify({
                    "success": False,
                    "message": "Akun tidak ditemukan"
                }), 404

            if jabatan:
                if karyawan.jabatan.nama_jabatan not in jabatan:
                    return jsonify({
                        "success": False,
                        "message": "Tidak punya akses (jabatan)"
                    }), 403

            if departemen:
                if karyawan.departemen.nama_departemen not in departemen:
                    return jsonify({
                        "success": False,
                        "message": "Tidak punya akses (departemen)"
                    }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
