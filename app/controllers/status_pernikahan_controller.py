from flask import request, jsonify
from app import db
from app.models.status_pernikahan import StatusPernikahan
from app.dto.status_pernikahan_dto import CreateStatusPernikahanDTO, UpdateStatusPernikahanDTO
import uuid

class StatusPernikahanController:

    @staticmethod
    def get_all():
        data = StatusPernikahan.query.all()
        return jsonify({
            "success": True,
            "data": [item.to_dict() for item in data]
        }), 200

    @staticmethod
    def get_by_id(id):
        item = StatusPernikahan.query.get(id)
        if not item:
            return jsonify({
                "success": False,
                "message": "Data tidak ditemukan"
            }), 404

        return jsonify({
            "success": True,
            "data": item.to_dict()
        }), 200

    @staticmethod
    def create():
        body = request.json or {}
        dto = CreateStatusPernikahanDTO(body)

        if not dto.nama:
            return jsonify({
                "success": False,
                "message": "Field 'nama' wajib diisi"
            }), 400

        new_item = StatusPernikahan(
            id=str(uuid.uuid4()),
            nama=dto.nama
        )

        db.session.add(new_item)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Status Pernikahan berhasil dibuat",
            "data": new_item.to_dict()
        }), 201

    @staticmethod
    def update(id):
        body = request.json or {}
        dto = UpdateStatusPernikahanDTO(body)

        item = StatusPernikahan.query.get(id)
        if not item:
            return jsonify({
                "success": False,
                "message": "Data tidak ditemukan"
            }), 404

        if dto.nama:
            item.nama = dto.nama

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Status Pernikahan berhasil diupdate",
            "data": item.to_dict()
        }), 200

    @staticmethod
    def delete(id):
        item = StatusPernikahan.query.get(id)
        if not item:
            return jsonify({
                "success": False,
                "message": "Data tidak ditemukan"
            }), 404

        db.session.delete(item)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Data berhasil dihapus"
        }), 200
