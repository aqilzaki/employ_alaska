import uuid
import os
from datetime import date, datetime
from flask import jsonify, request,current_app
from app.utils.request_data import get_request_data

from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.transaksi_absensi import TransaksiAbsensi
from app.models.karyawan import Karyawan
from app.dto.absensi_dto import (
    absensi_schema,
    absensi_in_schema,
    absensi_out_schema
)
from app.middlewares.role_required import role_required
from app.middlewares.active_account_required import active_account_required


class AbsensiOperatorController:

        @staticmethod
        @jwt_required()
        @active_account_required
        @role_required(departemen=["OPERATOR", "CS"])
        def absen_in():
            identity = get_jwt_identity()
            data = get_request_data(include_files=True)
           
            print("DATA KE MARSHMALLOW:", data)
            print("FILES ASLI:", request.files)

            payload = absensi_in_schema.load(data)

            foto = payload["foto_in"]
            today = date.today()

            existing = TransaksiAbsensi.query.filter_by(
                id_karyawan=identity,
                tanggal=today
            ).first()

            if existing:
                return jsonify({
                    "success": False,
                    "message": "Sudah absen hari ini"
                }), 400

            # === SIMPAN FOTO ===
            ext = foto.filename.rsplit(".", 1)[1]
            filename = f"{uuid.uuid4()}.{ext}"

            folder = os.path.join(current_app.root_path, "static", "absensi", "in")
            os.makedirs(folder, exist_ok=True)

            foto.save(os.path.join(folder, filename))

            foto_path = f"/static/absensi/in/{filename}"

            data = TransaksiAbsensi(
                id=str(uuid.uuid4()),
                id_karyawan=identity,
                tanggal=today,
                jam_in=datetime.now().time(),
                foto_in=foto_path
            )

            db.session.add(data)
            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Absen IN berhasil",
                "data": absensi_schema.dump(data)
            }), 201
        
        @staticmethod
        @jwt_required()
        @active_account_required
        @role_required(departemen=["OPERATOR", "CS"])
        def absen_out():
            identity = get_jwt_identity()
            request_data = get_request_data(include_files=True)

            payload = absensi_out_schema.load(request_data)
            foto = payload["foto_out"]
            today = date.today()

            data = TransaksiAbsensi.query.filter_by(
                id_karyawan=identity,
                tanggal=today
            ).first()

            if not data:
                return jsonify({
                    "success": False,
                    "message":  "Belum absen IN"
                }), 400

            if data.jam_out:
                return jsonify({
                    "success": False,
                    "message": "Sudah absen OUT"
                }), 400

            # === SIMPAN FOTO ===
            ext = foto.filename.rsplit(".", 1)[1]
            filename = f"{uuid.uuid4()}.{ext}"
            folder = os.path.join(current_app.root_path, "static", "absensi", "out")
            os.makedirs(folder, exist_ok=True)
            foto.save(os.path.join(folder, filename))
            foto_path = f"/static/absensi/out/{filename}"


            data.jam_out = datetime.now().time()
            data.foto_out = foto_path
            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Absen OUT berhasil",
                "data": absensi_schema.dump(data)
            }), 200
