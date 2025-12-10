from flask import jsonify, request
from app import db
from app.models.jabatan import Jabatan
from app.dto.jabatan_dto import (
    jabatan_schema, 
    jabatan_list_schema, 
    jabatan_create_schema, 
    jabatan_update_schema
)
from marshmallow import ValidationError

class JabatanController:
    
    @staticmethod
    def get_all():
        """Get all jabatan"""
        try:
            jabatan_list = Jabatan.query.all()
            result = jabatan_list_schema.dump(jabatan_list)
            return jsonify({
                'success': True,
                'message': 'Data jabatan berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
    
    @staticmethod
    def get_by_id(id):
        """Get jabatan by ID"""
        try:
            jabatan = Jabatan.query.get(id)
            if not jabatan:
                return jsonify({
                    'success': False,
                    'message': 'Jabatan tidak ditemukan'
                }), 404
            
            result = jabatan_schema.dump(jabatan)
            return jsonify({
                'success': True,
                'message': 'Data jabatan berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
    
    @staticmethod
    def create():
        """Create new jabatan"""
        try:
            data = request.get_json()
            
            # Validate data
            validated_data = jabatan_create_schema.load(data)
            
            last = Jabatan.query.order_by(Jabatan.id.desc()).first()

            if last:
                try:
                    last_id_num = int(last.id.split('-')[1])
                    new_id_num = last_id_num + 1
                except (IndexError, ValueError):
                    new_id_num = 1
            else:
                new_id_num = 1
            new_id = f"JBT-{new_id_num:04d}"
            validated_data['id'] = new_id

            # Check if ID already exists
            existing = Jabatan.query.get(validated_data['id'])
            if existing:
                return jsonify({
                    'success': False,
                    'message': 'ID jabatan sudah digunakan'
                }), 400
            
            # Create new jabatan
            new_jabatan = Jabatan(**validated_data)
            db.session.add(new_jabatan)
            db.session.commit()
            
            result = jabatan_schema.dump(new_jabatan)
            return jsonify({
                'success': True,
                'message': 'Jabatan berhasil ditambahkan',
                'data': result
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
        """Update jabatan by ID"""
        try:
            jabatan = Jabatan.query.get(id)
            if not jabatan:
                return jsonify({
                    'success': False,
                    'message': 'Jabatan tidak ditemukan'
                }), 404
            
            data = request.get_json()
            
            # Validate data
            validated_data = jabatan_update_schema.load(data)
            
            # Update fields
            for key, value in validated_data.items():
                setattr(jabatan, key, value)
            
            db.session.commit()
            
            result = jabatan_schema.dump(jabatan)
            return jsonify({
                'success': True,
                'message': 'Jabatan berhasil diupdate',
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
        """Delete jabatan by ID"""
        try:
            jabatan = Jabatan.query.get(id)
            if not jabatan:
                return jsonify({
                    'success': False,
                    'message': 'Jabatan tidak ditemukan'
                }), 404
            
            # Check if jabatan is used by karyawan
            if jabatan.karyawan:
                return jsonify({
                    'success': False,
                    'message': 'Jabatan tidak dapat dihapus karena masih digunakan oleh karyawan'
                }), 400
            
            db.session.delete(jabatan)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Jabatan berhasil dihapus'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500