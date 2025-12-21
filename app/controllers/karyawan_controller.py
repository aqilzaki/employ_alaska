from flask import jsonify, request
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash

from app.models.karyawan import Karyawan
from app.models.jabatan import Jabatan
from app.models.status_kerja import StatusKerja
from app.models.status_pernikahan import StatusPernikahan
from app.models.kondisi_akun import kondisiAkun
from app.dto.karyawan_dto import (
    karyawan_schema, 
    karyawan_list_schema, 
    karyawan_create_schema, 
    karyawan_update_schema,
)
from marshmallow import ValidationError
import traceback
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
        """Create new karyawan (ID manual + debug error)"""
        try:
            data = request.get_json()

            try:
                # --- HITUNG DURASI KONTRAK ---
                awal_kontrak = datetime.strptime(data.get('awal_kontrak'), "%Y-%m-%d").date()
                akhir_kontrak = datetime.strptime(data.get('akhir_kontrak'), "%Y-%m-%d").date()
                data['durasi_kontrak'] = (akhir_kontrak - awal_kontrak).days
            except Exception as e:
                return jsonify({
                    "success": False,
                    "step": "Menghitung durasi kontrak",
                    "error": str(e),
                    "trace": traceback.format_exc()
                }), 400

            try:
                validated_data = karyawan_create_schema.load(data)
            except ValidationError as e:
                return jsonify({
                    "success": False,
                    "step": "Validasi schema",
                    "message": "Validasi gagal",
                    "errors": e.messages
                }), 400
            except Exception as e:
                return jsonify({
                    "success": False,
                    "step": "Validasi schema (unexpected)",
                    "error": str(e),
                    "trace": traceback.format_exc()
                }), 400

            # ---------- CEK DUPLIKAT ID ----------
            try:
                existing_id = Karyawan.query.get(validated_data['id'])
                if existing_id:
                    return jsonify({
                        "success": False,
                        "step": "Cek ID duplikat",
                        "message": "ID karyawan sudah digunakan"
                    }), 400
            except Exception as e:
                return jsonify({
                    "success": False,
                    "step": "Cek ID duplikat",
                    "error": str(e),
                    "trace": traceback.format_exc()
                }), 400

            # ---------- CEK DUPLIKAT NIK ----------
            try:
                existing_nik = Karyawan.query.filter_by(nik=validated_data['nik']).first()
                if existing_nik:
                    return jsonify({
                        "success": False,
                        "step": "Cek NIK duplikat",
                        "message": "NIK sudah terdaftar"
                    }), 400
            except Exception as e:
                return jsonify({
                    "success": False,
                    "step": "Cek NIK duplikat",
                    "error": str(e),
                    "trace": traceback.format_exc()
                }), 400

            # ---------- VALIDASI FOREIGN KEY ----------
            fk_checks = {
                "id_jabatan_karyawan": "Jabatan tidak ditemukan",
                "id_status_pernikahan": "Status pernikahan tidak ditemukan",
                "id_status_kerja_karyawan": "Status kerja tidak ditemukan",
            }

            for key, error_message in fk_checks.items():
                try:
                    model = {
                        "id_jabatan_karyawan": Jabatan,
                        "id_status_pernikahan": StatusPernikahan,
                        "id_status_kerja_karyawan": StatusKerja,
                    }[key]

                    if not model.query.get(validated_data[key]):
                        return jsonify({
                            "success": False,
                            "step": f"Validasi foreign key: {key}",
                            "message": error_message
                        }), 400

                except Exception as e:
                    return jsonify({
                        "success": False,
                        "step": f"Validasi foreign key: {key}",
                        "error": str(e),
                        "trace": traceback.format_exc()
                    }), 400

            # ---------- SIMPAN DATA ----------
            try:
                password_plain = "Alaska11"  # Set a default password or generate one
                validated_data['password'] = generate_password_hash(password_plain) # In real app, hash this password
                new_karyawan = Karyawan(**validated_data)
                db.session.add(new_karyawan)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    "success": False,
                    "step": "Insert ke database",
                    "error": str(e),
                    "trace": traceback.format_exc()
                }), 500

            return jsonify({
                "success": True,
                "message": "Karyawan berhasil ditambahkan",
                "data": {
                    "id": new_karyawan.id,
                    "nama": new_karyawan.nama
                }
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "step": "General exception (outer)",
                "error": str(e),
                "trace": traceback.format_exc()
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
                if status.nama_status == 'BERHENTI':
                   karyawan.id_kondisi_akun = "KA-0002" # Set kondisi akun to non-aktif
                if status.nama_status in ('TETAP', 'KONTRAK'):
                   karyawan.id_kondisi_akun = "KA-0001"
            
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
        

    @staticmethod
    def update_kondisi_akun_karyawan(id_karyawan):
        """Update kondisi akun for a karyawan"""
        try:
            karyawan = Karyawan.query.get(id_karyawan)
            if not karyawan:
                return jsonify({
                    'success': False,
                    'message': 'Karyawan tidak ditemukan'
                }), 404

            Karyawan.id_kondisi_akun = "KA-0002"  # Set to non-aktif
            db.session.commit()

            result = karyawan_schema.dump(karyawan)
            return jsonify({
                'success': True,
                'message': 'Kondisi akun karyawan berhasil diupdate',
                'data': result
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}'
            }), 500
        
    @staticmethod
    def get_all_karyawan_by_kondisi_non_aktif():
            """Get all karyawan by kondisi akun non-aktif"""
            try:
                karyawan_list = Karyawan.query.filter_by(id_kondisi_akun="KA-0002").all()
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