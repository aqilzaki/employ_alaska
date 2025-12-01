from flask import jsonify, request
from app import db
from datetime import datetime
from app.models.karyawan import Karyawan
from app.models.jabatan import Jabatan
from app.models.status_kerja import StatusKerja
from app.models.status_pernikahan import StatusPernikahan
from app.dto.karyawan_dto import (
    karyawan_schema, 
    karyawan_list_schema, 
    karyawan_create_schema, 
    karyawan_update_schema
)
from marshmallow import ValidationError

class KaryawanController:
    
    @staticmethod
    def get_all():
        """Get all karyawan with filters"""
        try:
            # Get query parameters for filtering
            jabatan_id = request.args.get('jabatan')
            status_id = request.args.get('status')
            search = request.args.get('search')
            
            # Base query
            query = Karyawan.query
            
            # Apply filters
            if jabatan_id:
                query = query.filter_by(id_jabatan_karyawan=jabatan_id)
            if status_id:
                query = query.filter_by(id_status_kerja_karyawan=status_id)
            if search:
                query = query.filter(
                    (Karyawan.nama.like(f'%{search}%')) | 
                    (Karyawan.nik.like(f'%{search}%'))
                )
            
            karyawan_list = query.all()
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
    
    @staticmethod
    def get_by_id(id):
        """Get karyawan by ID"""
        try:
            karyawan = Karyawan.query.get(id)
            if not karyawan:
                return jsonify({
                    'success': False,
                    'message': 'Karyawan tidak ditemukan'
                }), 404
            
            result = karyawan_schema.dump(karyawan)
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
    
    @staticmethod
    def create():
        """Create new karyawan with auto-generated ID"""
        try:
            data = request.get_json()
            
            # ✅ AUTO-GENERATE ID
            # Ambil karyawan terakhir berdasarkan ID
            last_employee = Karyawan.query.order_by(Karyawan.id.desc()).first()
            
            if last_employee and last_employee.id.startswith('KRY'):
                # Extract nomor dari ID terakhir (misal: KRY005 -> 5)
                try:
                    last_number = int(last_employee.id.replace('KRY', ''))
                    new_number = last_number + 1
                except ValueError:
                    # Kalau gagal parse, mulai dari 1
                    new_number = 1
            else:
                # Kalau belum ada data, mulai dari 1
                new_number = 1
            
            # Format dengan leading zeros (001, 002, 003, ...)
            new_id = f'KRY{new_number:03d}'
            
            # ✅ Remove 'id' dari data request (kalau ada), backend yang handle
            if 'id' in data:
                del data['id']
            
            # Set ID baru
            data['id'] = new_id

           # --- HITUNG DURASI KONTRAK ---
            awal_kontrak = datetime.strptime(data.get('awal_kontrak'), "%Y-%m-%d").date()
            akhir_kontrak = datetime.strptime(data.get('akhir_kontrak'), "%Y-%m-%d").date()

            durasi_kontrak = (akhir_kontrak - awal_kontrak).days
            data['durasi_kontrak'] = durasi_kontrak
            
            # Validate data
            validated_data = karyawan_create_schema.load(data)
            
            # Check if NIK already exists
            existing_nik = Karyawan.query.filter_by(nik=validated_data['nik']).first()
            if existing_nik:
                return jsonify({
                    'success': False,
                    'message': 'NIK sudah terdaftar'
                }), 400
            
            # Validate foreign keys
            jabatan = Jabatan.query.get(validated_data['id_jabatan_karyawan'])
            if not jabatan:
                return jsonify({
                    'success': False,
                    'message': 'Jabatan tidak ditemukan'
                }), 400
            
            status_pernikahan = StatusPernikahan.query.get(validated_data['id_status_pernikahan'])
            if not status_pernikahan:
                return jsonify({
                    'success': False,
                    'message': 'Status pernikahan tidak ditemukan'
                }), 400
            
            status = StatusKerja.query.get(validated_data['id_status_kerja_karyawan'])
            if not status:
                return jsonify({
                    'success': False,
                    'message': 'Status kerja tidak ditemukan'
                }), 400
            
            # Create new karyawan
            new_karyawan = Karyawan(**validated_data)
            db.session.add(new_karyawan)
            db.session.commit()
            
            # ✅ Return simple response (avoid nested serialization error)
            return jsonify({
                'success': True,
                'message': 'Karyawan berhasil ditambahkan',
                'data': {
                    'id': new_karyawan.id,
                    'nama': new_karyawan.nama
                }
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
        """Update karyawan by ID"""
        try:
            karyawan = Karyawan.query.get(id)
            if not karyawan:
                return jsonify({
                    'success': False,
                    'message': 'Karyawan tidak ditemukan'
                }), 404
            
            data = request.get_json()
            
            # Validate data
            validated_data = karyawan_update_schema.load(data)
            
            # Check if NIK is being updated and already exists
            if 'nik' in validated_data:
                existing_nik = Karyawan.query.filter_by(nik=validated_data['nik']).first()
                if existing_nik and existing_nik.id != id:
                    return jsonify({
                        'success': False,
                        'message': 'NIK sudah terdaftar'
                    }), 400
            
            # Validate foreign keys if being updated
            if 'id_jabatan_karyawan' in validated_data:
                jabatan = Jabatan.query.get(validated_data['id_jabatan_karyawan'])
                if not jabatan:
                    return jsonify({
                        'success': False,
                        'message': 'Jabatan tidak ditemukan'
                    }), 400
            
            if 'id_status_kerja_karyawan' in validated_data:
                status = StatusKerja.query.get(validated_data['id_status_kerja_karyawan'])
                if not status:
                    return jsonify({
                        'success': False,
                        'message': 'Status kerja tidak ditemukan'
                    }), 400
            
            # Update fields
            for key, value in validated_data.items():
                setattr(karyawan, key, value)
            
            db.session.commit()
            
            result = karyawan_schema.dump(karyawan)
            return jsonify({
                'success': True,
                'message': 'Karyawan berhasil diupdate',
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
        """Delete karyawan by ID"""
        try:
            karyawan = Karyawan.query.get(id)
            if not karyawan:
                return jsonify({
                    'success': False,
                    'message': 'Karyawan tidak ditemukan'
                }), 404
            
            db.session.delete(karyawan)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Karyawan berhasil dihapus'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500