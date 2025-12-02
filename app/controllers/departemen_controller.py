from flask import jsonify, request
from app import db
from app.models.departemen import Departemen
from app.dto.departemen_dto import (
    departemen_schema,
    departemen_list_schema,
    departemen_create_schema,
    departemen_update_schema
)
from marshmallow import ValidationError
import uuid

class DepartemenController:
    @staticmethod
    def get_all():
        """Get all departemen"""
        try:
            departemen_list = Departemen.query.all()
            result = departemen_list_schema.dump(departemen_list)
            return jsonify({
                'success': True,
                'message': 'Data departemen berhasil diambil',
                'data': result
            }), 200     
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
        
    @staticmethod
    def get_by_id(id):
        """Get departemen by ID"""
        try:
            departemen = Departemen.query.get(id)
            if not departemen:
                return jsonify({
                    'success': False,
                    'message': 'Departemen tidak ditemukan'
                }), 404
            
            result = departemen_schema.dump(departemen)
            return jsonify({    
                'success': True,
                'message': 'Data departemen berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
        
    @staticmethod
    def create():
        """Create new departemen"""
        try:
            data = request.get_json()
            
            # Validate data
            validated = departemen_create_schema.load(data)
            

            last = Departemen.query.order_by(Departemen.id.desc()).first()

            if last:
                try:
                    last_id_num = int(last.id.split('-')[1])
                    new_id_num = last_id_num + 1
                except (IndexError, ValueError):
                    new_id_num = 1
            else:
                new_id_num = 1
            new_id = f"DT-{new_id_num:04d}"

            # Create departemen
            new_departemen = Departemen(
                id=new_id,
                nama_departemen=validated['nama_departemen'],
            )
            db.session.add(new_departemen)
            db.session.commit()
            
            result = departemen_schema.dump(new_departemen)
            return jsonify({
                'success': True,
                'message': 'Departemen berhasil dibuat',
                'data': result
            }), 201
        except ValidationError as ve:
            return jsonify({
                'success': False,
                'message': 'Validasi data gagal',
                'errors': ve.messages
            }), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
        
    @staticmethod
    def update(id):
        """Update departemen by ID"""
        try:
            departemen = Departemen.query.get(id)
            if not departemen:
                return jsonify({
                    'success': False,
                    'message': 'Departemen tidak ditemukan'
                }), 404
            
            data = request.get_json()
            
            # Validate data
            validated = departemen_update_schema.load(data)
            
            # Update fields
            if 'nama_departemen' in validated:
                departemen.nama_departemen = validated['nama_departemen']
            if 'deskripsi' in validated:
                departemen.deskripsi = validated['deskripsi']
            db.session.commit()
            result = departemen_schema.dump(departemen)
            return jsonify({    
                'success': True,
                'message': 'Departemen berhasil diupdate',
                'data': result
            }), 200 
        except ValidationError as ve:
            return jsonify({
                'success': False,
                'message': 'Validasi data gagal',
                'errors': ve.messages
            }), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
        
    @staticmethod
    def delete(id):
        """Delete departemen by ID"""
        try:
            departemen = Departemen.query.get(id)
            if not departemen:
                return jsonify({
                    'success': False,
                    'message': 'Departemen tidak ditemukan'
                }), 404
            
            db.session.delete(departemen)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Departemen berhasil dihapus'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
        
    @staticmethod
    def get_karyawan_by_departemen(id):
        """Get all karyawan in a departemen"""
        try:
            departemen = Departemen.query.get(id)
            if not departemen:
                return jsonify({
                    'success': False,
                    'message': 'Departemen tidak ditemukan'
                }), 404
            
            karyawan_list = departemen.karyawan
            # Assuming you have a Karyawan schema to serialize karyawan data
            from app.dto.karyawan_dto import karyawan_list_schema
            result = karyawan_list_schema.dump(karyawan_list)
            return jsonify({
                'success': True,
                'message': 'Data karyawan berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500