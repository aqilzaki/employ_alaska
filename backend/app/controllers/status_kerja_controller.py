from flask import jsonify, request
from app import db
from app.models.status_kerja import StatusKerja
from app.dto.status_kerja_dto import (
    status_kerja_schema, 
    status_kerja_list_schema, 
    status_kerja_create_schema, 
    status_kerja_update_schema
)
from marshmallow import ValidationError

class StatusKerjaController:
    
    @staticmethod
    def get_all():
        """Get all status kerja"""
        try:
            status_list = StatusKerja.query.all()
            result = status_kerja_list_schema.dump(status_list)
            return jsonify({
                'success': True,
                'message': 'Data status kerja berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
    
    @staticmethod
    def get_by_id(id):
        """Get status kerja by ID"""
        try:
            status = StatusKerja.query.get(id)
            if not status:
                return jsonify({
                    'success': False,
                    'message': 'Status kerja tidak ditemukan'
                }), 404
            
            result = status_kerja_schema.dump(status)
            return jsonify({
                'success': True,
                'message': 'Data status kerja berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
    
    @staticmethod
    def create():
        """Create new status kerja"""
        try:
            data = request.get_json()
            
            # Validate data
            validated_data = status_kerja_create_schema.load(data)
            
            # Check if ID already exists
            existing = StatusKerja.query.get(validated_data['id'])
            if existing:
                return jsonify({
                    'success': False,
                    'message': 'ID status kerja sudah digunakan'
                }), 400
            
            # Create new status kerja
            new_status = StatusKerja(**validated_data)
            db.session.add(new_status)
            db.session.commit()
            
            result = status_kerja_schema.dump(new_status)
            return jsonify({
                'success': True,
                'message': 'Status kerja berhasil ditambahkan',
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
        """Update status kerja by ID"""
        try:
            status = StatusKerja.query.get(id)
            if not status:
                return jsonify({
                    'success': False,
                    'message': 'Status kerja tidak ditemukan'
                }), 404
            
            data = request.get_json()
            
            # Validate data
            validated_data = status_kerja_update_schema.load(data)
            
            # Update fields
            for key, value in validated_data.items():
                setattr(status, key, value)
            
            db.session.commit()
            
            result = status_kerja_schema.dump(status)
            return jsonify({
                'success': True,
                'message': 'Status kerja berhasil diupdate',
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
        """Delete status kerja by ID"""
        try:
            status = StatusKerja.query.get(id)
            if not status:
                return jsonify({
                    'success': False,
                    'message': 'Status kerja tidak ditemukan'
                }), 404
            
            # Check if status is used by karyawan
            if status.karyawan:
                return jsonify({
                    'success': False,
                    'message': 'Status kerja tidak dapat dihapus karena masih digunakan oleh karyawan'
                }), 400
            
            db.session.delete(status)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Status kerja berhasil dihapus'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500