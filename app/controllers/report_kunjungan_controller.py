from flask import jsonify, request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.kunjungan import Kunjungan
from app.models.karyawan import Karyawan
from app.dto.kunjungan_dto import report_kunjungan_schema

from app.middlewares.active_account_required import active_account_required


class ReportKunjunganController:

    @staticmethod
    @jwt_required()
    @active_account_required
    def get_kunjungan():
        identity = get_jwt_identity()
        user = Karyawan.query.get(identity)

        if not user:
            return jsonify({
                "success": False,
                "message": "Akun tidak ditemukan"
            }), 404

        # ======================
        # BASE QUERY
        # ======================
        query = Kunjungan.query.join(Kunjungan.karyawan)

        # ======================
        # ROLE SCOPE
        # ======================
        if user.departemen.nama_departemen == "HRD":
            pass  # semua data

        elif user.jabatan.nama_jabatan == "KETUA":
            query = query.filter(
                Karyawan.id_departemen == user.id_departemen
            )

        else:
            query = query.filter(
                Kunjungan.id_karyawan == identity
            )

        # ======================
        # FILTER TANGGAL
        # ======================
        tanggal = request.args.get("tanggal")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if tanggal:
            tanggal = datetime.strptime(tanggal, "%Y-%m-%d").date()
            query = query.filter(Kunjungan.tanggal == tanggal)

        if start_date and end_date:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            query = query.filter(Kunjungan.tanggal.between(start, end))

        data = query.order_by(
            Kunjungan.tanggal.desc()
        ).all()

        if not data:
            return jsonify({
                "success": False,
                "message": "Data kunjungan tidak ditemukan"
            }), 404

        return jsonify({
            "success": True,
            "data": report_kunjungan_schema.dump(data, many=True)
        }), 200
