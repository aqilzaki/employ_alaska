from datetime import date, datetime
import os
import uuid
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.karyawan import Karyawan
from app.dto.izin_dto import IzinSchema
from app.models.status_request import StatusRequest
from app.utils.request_data import get_request_data
from app import db
from app.models.izin_operator import IzinOperator
from app.middlewares.role_required import role_required
from app.middlewares.active_account_required import active_account_required

class IzinController:

    @staticmethod
    @jwt_required()
    @active_account_required
    @role_required(departemen=["OPERATOR"])
    def ajukan_izin():
        identity = get_jwt_identity()
        request_data = get_request_data(include_files=True)

        foto = request_data.get("foto")
        tanggal = request_data.get("tanggal") or date.today()

        if isinstance(tanggal, str):
            tanggal = date.fromisoformat(tanggal)

        # ===== CEK SUDAH IZIN DI TANGGAL ITU =====
        existing = IzinOperator.query.filter(
            IzinOperator.id_karyawan == identity,
            IzinOperator.tanggal == tanggal,
            # IzinOperator.id_status.in_(
            #     StatusRequest.query.with_entities(StatusRequest.id)
            # )
            IzinOperator.id_status == 2  # KODE APPROVED
        ).first()

        if existing:
            return jsonify({
                "success": False,
                "message": "Sudah mengajukan izin di tanggal ini"
            }), 400

    

        foto_path = None
        if foto:
            if "." not in foto.filename:
                return jsonify({
                    "success": False,
                    "message": "File foto tidak valid"
                }), 400

            ext = foto.filename.rsplit(".", 1)[1]
            filename = f"{identity}_{datetime.now().timestamp()}.{ext}"

            folder = current_app.root_path + "/static/izin"
            os.makedirs(folder, exist_ok=True)

            foto.save(f"{folder}/{filename}")
            foto_path = f"/static/izin/{filename}"

        izin = IzinOperator(
            id_karyawan=identity,
            tanggal=tanggal,
            jam=datetime.now().time(),
            foto=foto_path,
            keterangan=request_data.get("keterangan"),
        )

        db.session.add(izin)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Pengajuan izin berhasil"
        }), 201

    @staticmethod
    @jwt_required()
    @active_account_required
    @role_required(jabatan=["KETUA","AREA EKSEKUTIF", "MARKETING"])
    def update_status(id):
        identity = get_jwt_identity()
        user = Karyawan.query.get_or_404(identity)
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "message": "Body JSON wajib diisi"
            }), 400

        status_kode = data.get("status")

        if not status_kode:
            return jsonify({
                "success": False,
                "message": "Field 'status' wajib diisi"
            }), 400


        izin = (
            IzinOperator.query
            .join(Karyawan, IzinOperator.id_karyawan == Karyawan.id)
            .filter(IzinOperator.id == id)
            .first_or_404()
        )

        # ===== VALIDASI DEPARTEMEN =====
        if user.departemen.nama_departemen != "HRD":
            if izin.karyawan.id_departemen != user.id_departemen:
                return jsonify({
                    "success": False,
                    "message": "Tidak berhak memproses izin ini"
                }), 403

        status = StatusRequest.query.filter_by(
            kode=status_kode
        ).first_or_404()

        izin.id_status = status.id
        izin.approved_by = identity

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Status izin diperbarui"
        }), 200



    @staticmethod
    @jwt_required()
    @active_account_required
    def get_my_history_izin():
        identity = get_jwt_identity()
        user = Karyawan.query.get_or_404(identity)

        status = request.args.get("status")
        start_date = request.args.get("from")
        end_date = request.args.get("to")
        departemen = request.args.get("departemen")

        query = IzinOperator.query.join(Karyawan)

        # ===== ROLE BASE ACCESS =====
        if user.jabatan.nama_jabatan == "HRD":
            # HRD boleh semua
            if departemen:
                query = query.filter(
                    Karyawan.departemen.has(nama_departemen=departemen)
                )

        elif user.jabatan.nama_jabatan == "KETUA":
            # Ketua hanya departemennya
            query = query.filter(
                Karyawan.id_departemen == user.id_departemen
            )

        else:
            # User biasa hanya miliknya
            query = query.filter(
                IzinOperator.id_karyawan == identity
            )

        # ===== FILTER STATUS =====
        if status:
            status_obj = StatusRequest.query.filter_by(kode=status).first()
            if not status_obj:
                return jsonify({
                    "success": False,
                    "message": "Status tidak valid"
                }), 400

            query = query.filter(
                IzinOperator.id_status == status_obj.id
            )

        # ===== FILTER TANGGAL =====
        if start_date:
            query = query.filter(
                IzinOperator.tanggal >= start_date
            )

        if end_date:
            query = query.filter(
                IzinOperator.tanggal <= end_date
            )

        results = query.order_by(
            IzinOperator.created_at.desc()
        ).all()

        if not results:
            return jsonify({
                "success": False,
                "message": "Data izin tidak ditemukan"
            }), 404

        return jsonify({
            "success": True,
            "message": "Data izin berhasil didapatkan",
            "data": IzinSchema(many=True).dump(results)
        }), 200
