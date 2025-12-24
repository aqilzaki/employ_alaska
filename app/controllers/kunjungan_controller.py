import os
from datetime import date, datetime
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.kunjungan import Kunjungan
from app.models.kunjungan_foto import KunjunganFoto
from app.dto.kunjungan_dto import (
    kunjungan_schema,
    kunjungan_foto_create_schema
)
from app.utils.request_data import get_request_data
from app.middlewares.role_required import role_required
from app.middlewares.active_account_required import active_account_required


class KunjunganController:

    @staticmethod
    @jwt_required()
    @active_account_required
    @role_required(departemen=["AREA EKSEKUTIF", "SALES"])
    def submit_kunjungan():
        identity = get_jwt_identity()
        today = date.today()

        data = get_request_data(include_files=True)
        payload = kunjungan_foto_create_schema.load(data)

        foto = payload["foto"]
        latitude = payload["latitude"]
        longitude = payload["longitude"]

        # =====================
        # CARI / BUAT KUNJUNGAN
        # =====================
        kunjungan = Kunjungan.query.filter_by(
            id_karyawan=identity,
            tanggal=today
        ).first()

        if not kunjungan:
            kunjungan = Kunjungan(
                id_karyawan=identity,
                tanggal=today
            )
            db.session.add(kunjungan)
            db.session.commit()

        # =====================
        # VALIDASI FOTO
        # =====================
        if len(kunjungan.fotos) >= 5:
            return jsonify({
                "success": False,
                "message": "Maksimal 5 foto kunjungan per hari"
            }), 400

        # =====================
        # SIMPAN FOTO
        # =====================
        ext = foto.filename.rsplit(".", 1)[1]
        filename = f"{kunjungan.id}_{len(kunjungan.fotos)+1}.{ext}"

        folder = os.path.join(
            current_app.root_path,
            "static",
            "kunjungan"
        )
        os.makedirs(folder, exist_ok=True)

        foto.save(os.path.join(folder, filename))
        foto_path = f"/static/kunjungan/{filename}"

        foto_db = KunjunganFoto(
            id_kunjungan=kunjungan.id,
            foto=foto_path,
            latitude=latitude,
            longitude=longitude,
            jam=datetime.now().time()
        )

        db.session.add(foto_db)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Foto kunjungan berhasil disimpan",
            "total_foto": len(kunjungan.fotos),
            "data": kunjungan_schema.dump(kunjungan)
        }), 201
