from flask import request, jsonify
from marshmallow import ValidationError
from werkzeug.security import check_password_hash
from flask_jwt_extended import (create_access_token,jwt_required,
    get_jwt,
    get_jwt_identity,
    create_access_token)

from app import db
from app.models.karyawan import Karyawan
from app.dto.auth_dto import login_schema
from app.models.jwt_blacklist import TokenBlacklist


class AuthController:

    @staticmethod
    def login():
        json_data = request.get_json()

        # =========================
        # VALIDASI DTO
        # =========================
        try:
            data = login_schema.load(json_data)
        except ValidationError as err:
            return jsonify({
                "success": False,
                "message": "Validasi gagal",
                "errors": err.messages
            }), 400

        # =========================
        # AMBIL KARYAWAN
        # =========================
        karyawan = Karyawan.query.filter_by(id=data["id"]).first()

        if not karyawan:
            return jsonify({
                "success": False,
                "message": "Karyawan tidak ditemukan"
            }), 404

        # =========================
        # CEK KONDISI AKUN
        # =========================
        if karyawan.kondisi_akun.nama_kondisi_akun.lower() != "aktif":
            return jsonify({
                "success": False,
                "message": "Akun tidak aktif"
            }), 403

        # =========================
        # CEK STATUS KERJA
        # =========================
        if karyawan.status_kerja.nama_status.lower() == "berhenti":
            return jsonify({
                "success": False,
                "message": "Status kerja sudah berhenti"
            }), 403

        # =========================
        # CEK PASSWORD
        # =========================
        if not check_password_hash(karyawan.password, data["password"]):
            return jsonify({
                "success": False,
                "message": "Password salah"
            }), 401

        # =========================
        # JWT CLAIMS (ROLE)
        # =========================
        additional_claims = {
            "jabatan": karyawan.jabatan.nama_jabatan,
            "departemen": karyawan.departemen.nama_departemen,
            "status_kerja": karyawan.status_kerja.nama_status
        }

        access_token = create_access_token(
            identity=karyawan.id,
            additional_claims=additional_claims
        )

        return jsonify({
            "success": True,
            "message": "Login berhasil",
            "access_token": access_token
        }), 200


    @staticmethod
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        jwt_data = get_jwt()

        additional_claims = {
            "jabatan": jwt_data.get("jabatan"),
            "departemen": jwt_data.get("departemen"),
            "status_kerja": jwt_data.get("status_kerja")
        }

        new_access_token = create_access_token(
            identity=identity,
            additional_claims=additional_claims
        )

        return jsonify({
            "success": True,
            "access_token": new_access_token
        }), 200

    @staticmethod
    @jwt_required()
    def logout():
        jwt_data = get_jwt()
        jti = jwt_data["jti"]

        db.session.add(TokenBlacklist(jti=jti))
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Logout berhasil"
        }), 200