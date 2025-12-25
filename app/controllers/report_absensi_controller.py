from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.models.transaksi_absensi import TransaksiAbsensi
from app.models.karyawan import Karyawan
from app.dto.absensi_dto import AbsensiReportSchema, absensi_schema
from app import db
from app.middlewares.role_required import role_required
from app.middlewares.active_account_required import active_account_required


class ReportAbsensiController:

    @staticmethod
    @jwt_required()
    @active_account_required
    @role_required(
        jabatan=["KETUA"],
        departemen=["HRD", "OPERATOR", "CS", "AREA EKSEKUTIF"]
    )
    def report_absensi():
        identity = get_jwt_identity()
        user = Karyawan.query.get(identity)

        # =====================
        # QUERY PARAMS
        # =====================
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        bulan = request.args.get("bulan")          # YYYY-MM
        departemen_filter = request.args.get("departemen")

        query = TransaksiAbsensi.query.join(
            TransaksiAbsensi.karyawan
        )

        # =====================
        # ROLE LOGIC
        # =====================
        if user.departemen.nama_departemen == "HRD":
            # HRD boleh filter departemen
            if departemen_filter:
                query = query.filter(
                    Karyawan.departemen.has(
                        nama_departemen=departemen_filter
                    )
                )
        else:
            # Ketua → departemen sendiri
            query = query.filter(
                Karyawan.id_departemen == user.id_departemen
            )

        # =====================
        # FILTER TANGGAL
        # =====================
        if start_date and end_date:
            query = query.filter(
                TransaksiAbsensi.tanggal.between(start_date, end_date)
            )

        # =====================
        # FILTER BULAN
        # =====================
        if bulan:
            start = datetime.strptime(bulan + "-01", "%Y-%m-%d").date()
            if start.month == 12:
                end = start.replace(year=start.year + 1, month=1)
            else:
                end = start.replace(month=start.month + 1)

            query = query.filter(
                TransaksiAbsensi.tanggal >= start,
                TransaksiAbsensi.tanggal < end
            )

        absensis = query.order_by(
            TransaksiAbsensi.tanggal.desc()
        ).all()

        if not absensis:
            return jsonify({
                "success": False,
                "message": "Data absensi tidak ditemukan"
            }), 404

        return jsonify({
            "success": True,
            "total": len(absensis),
            "data": AbsensiReportSchema.dump(absensis, many=True)
        }), 200


    @staticmethod
    @jwt_required()
    @active_account_required
    def get_my_absensi():
        identity = get_jwt_identity()

        # optional filter
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        bulan = request.args.get("bulan")  # format: YYYY-MM

        query = TransaksiAbsensi.query.filter(
            TransaksiAbsensi.id_karyawan == identity
        )

        if start_date and end_date:
            query = query.filter(
                TransaksiAbsensi.tanggal.between(start_date, end_date)
            )

        if bulan:
            year, month = bulan.split("-")
            query = query.filter(
                db.extract("year", TransaksiAbsensi.tanggal) == int(year),
                db.extract("month", TransaksiAbsensi.tanggal) == int(month)
            )

        data = query.order_by(TransaksiAbsensi.tanggal.desc()).all()

        if not data:
            return jsonify({
                "success": False,
                "message": "Data absensi tidak ditemukan"
            }), 404

        return jsonify({
            "success": True,
            "data": absensi_schema.dump(data, many=True)
        }), 200