from flask import jsonify, request
from app import db
from app.models.kondisi_akun import kondisiAkun
from app.dto.kondisi_akun_dto import (
    kondisi_akun_schema,
    kondisi_akun_list_schema,
    kondisi_akun_create_schema,
    kondisi_akun_update_schema
)
from marshmallow import ValidationError

class KondisiAkunController:

    @staticmethod
    def get_all():
        try:
            data = kondisiAkun.query.all()
            result = kondisi_akun_list_schema.dump(data)
            return jsonify({
                'success': True,
                'message': 'Data kondisi akun berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500

    @staticmethod
    def get_by_id(id):
        try:
            item = kondisiAkun.query.get(id)
            if not item:
                return jsonify({
                    'success': False,
                    'message': 'Kondisi akun tidak ditemukan'
                }), 404

            result = kondisi_akun_schema.dump(item)
            return jsonify({
                'success': True,
                'message': 'Data kondisi akun berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500

    @staticmethod
    def create():
        try:
            data = request.get_json()

            # Validasi input (tanpa id)
            validated = kondisi_akun_create_schema.load(data)

            # 🔥 AUTO GENERATE ID KA-0001
            last = kondisiAkun.query.order_by(kondisiAkun.id.desc()).first()

            if last:
                try:
                    last_number = int(last.id.replace("KA-", ""))
                    new_number = last_number + 1
                except:
                    new_number = 1
            else:
                new_number = 1

            new_id = f"KA-{new_number:04d}"

            # Tambahkan id ke validated data
            validated['id'] = new_id

            # Buat data baru
            new_item = kondisiAkun(**validated)
            db.session.add(new_item)
            db.session.commit()

            result = kondisi_akun_schema.dump(new_item)
            return jsonify({
                'success': True,
                'message': 'Kondisi akun berhasil ditambahkan',
            }), 201

        except ValidationError as e:
            return jsonify({
                'success': False,
                'message': 'Validasi gagal',
                'errors': e.messages
            }), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500

    @staticmethod
    def update(id):
        try:
            item = kondisiAkun.query.get(id)
            if not item:
                return jsonify({
                    'success': False,
                    'message': 'Kondisi akun tidak ditemukan'
                }), 404

            data = request.get_json()
            validated = kondisi_akun_update_schema.load(data)

            for key, value in validated.items():
                setattr(item, key, value)

            db.session.commit()

            result = kondisi_akun_schema.dump(item)
            return jsonify({
                'success': True,
                'message': 'Kondisi akun berhasil diupdate',
                'data': result
            }), 200

        except ValidationError as e:
            return jsonify({
                'success': False,
                'message': 'Validasi gagal',
                'errors': e.messages
            }), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500

    @staticmethod
    def delete(id):
        try:
            item = kondisiAkun.query.get(id)
            if not item:
                return jsonify({
                    'success': False,
                    'message': 'Kondisi akun tidak ditemukan'
                }), 404

            # Tidak boleh hapus jika dipakai karyawan
            if item.karyawan:
                return jsonify({
                    'success': False,
                    'message': 'Kondisi akun tidak dapat dihapus karena masih digunakan oleh karyawan'
                }), 400

            db.session.delete(item)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Kondisi akun berhasil dihapus'
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
