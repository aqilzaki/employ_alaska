from flask import request, jsonify
from app import db
from app.models.status_pernikahan import StatusPernikahan
from app.dto.status_pernikahan_dto import (
    status_pernikahan_schema,
    status_pernikahan_list_schema,
    status_pernikahan_create_schema,
    status_pernikahan_update_schema
)
from marshmallow import ValidationError


class StatusPernikahanController:

    @staticmethod
    def get_all():
        try:
            items = StatusPernikahan.query.all()
            result = status_pernikahan_list_schema.dump(items)
            return jsonify({
                "success": True,
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500

    @staticmethod
    def get_by_id(id):
        item = StatusPernikahan.query.get(id)
        if not item:
            return jsonify({
                "success": False,
                "message": "Data tidak ditemukan"
            }), 404

        result = status_pernikahan_schema.dump(item)
        return jsonify({
            "success": True,
            "data": result
        }), 200

    @staticmethod
    def create():
        try:
            data = request.json or {}
        
            validated = status_pernikahan_create_schema.load(data)

            last = StatusPernikahan.query.order_by(StatusPernikahan.id.desc()).first()

            if last:
                    try:
                        last_id_num = int(last.id.split('-')[2])
                        new_id_num = last_id_num + 1
                    except (IndexError, ValueError):
                        new_id_num = 1
            else:
                    new_id_num = 1
            new_id = f"ST-PERNI-{new_id_num:04d}"
            validated['id'] = new_id

            new_item = StatusPernikahan(
                id=new_id,
                nama=validated['nama']
            )

            db.session.add(new_item)
            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Status Pernikahan berhasil dibuat",
                "data": new_item.to_dict()
            }), 201
        except ValidationError as e:
            return jsonify({
                "success": False,
                "message": "Validasi data gagal",
                "errors": e.messages
            }), 400
    
    @staticmethod
    def update(id):
        try:
            item = StatusPernikahan.query.get(id)
            if not item:
                return jsonify({
                    "success": False,
                    "message": "Data tidak ditemukan"
                }), 404

            data = request.json or {}
            validated = status_pernikahan_update_schema.load(data)

            if 'nama_status_pernikahan' in validated:
                item.nama = validated['nama']

            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Status Pernikahan berhasil diperbarui",
                "data": item.to_dict()
            }), 200
        except ValidationError as e:
            return jsonify({
                "success": False,
                "message": "Validasi data gagal",
                "errors": e.messages
            }), 400

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
            "message": "Status Pernikahan berhasil dihapus"
        }), 200