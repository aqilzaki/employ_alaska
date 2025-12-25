import os
import uuid
from datetime import date, datetime
from flask import jsonify , request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.request_data import get_request_data

from app import db
from app.models.transaksi_absensi import TransaksiAbsensi
from app.models.kunjungan import Kunjungan
from app.middlewares.role_required import role_required
from app.middlewares.active_account_required import active_account_required
from app.dto.absensi_dto import absensi_out_schema, absensi_schema

class AbsensiAEController:

    @staticmethod
    @jwt_required()
    @active_account_required
    @role_required(departemen=["AREA EKSEKUTIF"])
    def absen_out_ae():
        identity = get_jwt_identity()
        request_data = get_request_data(include_files=True)
        payload = absensi_out_schema.load(request_data)  # Jika ada validasi tambahan, bisa ditambahkan di sini
        foto = payload["foto_out"]
        today = date.today()

        # =====================
        # CEK ABSENSI
        # =====================
        absensi = TransaksiAbsensi.query.filter_by(
            id_karyawan=identity,
            tanggal=today
        ).first()

        if not absensi:
            return jsonify({
                "success": False,
                "message": "Belum absen IN hari ini"
            }), 400

        if absensi.jam_out:
            return jsonify({
                "success": False,
                "message": "Sudah absen OUT"
            }), 400

        # =====================
        # CEK KUNJUNGAN
        # =====================
        kunjungan = Kunjungan.query.filter_by(
            id_karyawan=identity,
            tanggal=today
        ).first()

        if not kunjungan:
            return jsonify({
                "success": False,
                "message": "Belum ada kunjungan hari ini"
            }), 400

        total_foto = len(kunjungan.fotos)

        if total_foto < 5:
            return jsonify({
                "success": False,
                "message": f"Kunjungan belum lengkap (baru {total_foto}/5)"
            }), 400



        #simpan foto out
        ext = foto.filename.rsplit(".", 1)[1]
        filename = f"{uuid.uuid4()}.{ext}"
        folder = os.path.join(current_app.root_path, "static", "absensi", "out")
        os.makedirs(folder, exist_ok=True)
        foto.save(os.path.join(folder, filename))
        foto_path = f"/static/absensi/out/{filename}"
        # =====================
        # ABSEN OUT
        # =====================
        absensi.jam_out = datetime.now().time()
        absensi.foto_out = foto_path
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Absen OUT berhasil",
            "total_kunjungan": total_foto,
            "data": absensi_schema.dump(absensi)
        }), 200
