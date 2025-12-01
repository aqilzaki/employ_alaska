from flask import jsonify, request
from app import db
from app.models.agama import Agama
from app.dto.agama_dto import (
    agama_schema,
    agama_list_schema,
    agama_create_schema,
    agama_update_schema
)
from marshmallow import ValidationError

class AgamaController:
    @staticmethod
    def get_all():
        """Get all agama"""
        try:
            agama_list = Agama.query.all()
            result = agama_list_schema.dump(agama_list)
            return jsonify({
                'success': True,
                'message': 'Data agama berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
        
    @staticmethod
    def get_by_id(id):
        """Get agama by ID"""
        try:
            agama = Agama.query.get(id)
            if not agama:
                return jsonify({
                    'success': False,
                    'message': 'Agama tidak ditemukan'
                }), 404
            
            result = agama_schema.dump(agama)
            return jsonify({
                'success': True,
                'message': 'Data agama berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
    
    @staticmethod
    def create():
        """Create new agama"""
        try:
            data = request.get_json()
            
            # Validate data
            validated = agama_create_schema.load(data)
            
            last = Agama.query.order_by(Agama.id.desc()).first()

            if last:
                try:
                    last_id_num = int(last.id.split('-')[1])
                    new_id_num = last_id_num + 1
                except (IndexError, ValueError):
                    new_id_num = 1
            else:
                new_id_num = 1
            new_id = f"AG-{new_id_num:04d}"
            validated['id'] = new_id
            
            # Create new Agama instance
            new_agama = Agama(
                id=validated['id'],
                nama_agama=validated['nama_agama']
            )
            
            db.session.add(new_agama)
            db.session.commit()
            
            result = agama_schema.dump(new_agama)
            return jsonify({
                'success': True,
                'message': 'Agama berhasil ditambahkan',
                'data': result
            }), 201
        except ValidationError as e:
            return jsonify({
                'success': False,
                'message': 'Validasi gagal',
                'errors': e.messages
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
        
    @staticmethod
    def update(id):
        """Update agama by ID"""
        try:
            agama = Agama.query.get(id)
            if not agama:
                return jsonify({
                    'success': False,
                    'message': 'Agama tidak ditemukan'
                }), 404
            
            data = request.get_json()
            
            # Validate data
            validated = agama_update_schema.load(data)
            
            # Update fields
            if 'nama_agama' in validated:
                agama.nama_agama = validated['nama_agama']
            
            db.session.commit()
            
            result = agama_schema.dump(agama)
            return jsonify({
                'success': True,
                'message': 'Agama berhasil diupdate',
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
        """Delete agama by ID"""
        try:
            agama = Agama.query.get(id)
            if not agama:
                return jsonify({
                    'success': False,
                    'message': 'Agama tidak ditemukan'
                }), 404
            
            db.session.delete(agama)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Agama berhasil dihapus'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
    
