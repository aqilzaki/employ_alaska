from flask import jsonify, request
from app import db
from app.models.gaji_rule import GajiRule
from app.models.jabatan import Jabatan
from app.dto.gaji_rule_dto import (
    gaji_rule_schema,
    gaji_rule_list_schema,
    gaji_rule_create_schema,
    gaji_rule_update_schema
)
from marshmallow import ValidationError
import uuid

class GajiRuleController:
    
    @staticmethod
    def get_all():
        """Get all gaji rule"""
        try:
            rules = GajiRule.query.all()
            result = gaji_rule_list_schema.dump(rules)
            return jsonify({
                'success': True,
                'message': 'Data rule gaji berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

    @staticmethod
    def get_by_id(id):
        """Get gaji rule by ID"""
        try:
            rule = GajiRule.query.get(id)
            if not rule:
                return jsonify({
                    'success': False,
                    'message': 'Rule gaji tidak ditemukan'
                }), 404

            result = gaji_rule_schema.dump(rule)
            return jsonify({
                'success': True,
                'message': 'Data rule gaji berhasil diambil',
                'data': result
            }), 200
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

    @staticmethod
    def create():
        """Create new gaji rule"""
        try:
            data = request.get_json()
            validated = gaji_rule_create_schema.load(data)

            # cek jabatan ada atau tidak
            jabatan = Jabatan.query.get(validated['id_jabatan_karyawan'])
            if not jabatan:
                return jsonify({
                    'success': False,
                    'message': 'Jabatan tidak ditemukan'
                }), 400

            # Generate ID otomatis RUL-0001
            last = GajiRule.query.order_by(GajiRule.id.desc()).first()
            if last:
                try:
                    last_num = int(last.id.split('-')[1])
                    new_num = last_num + 1
                except:
                    new_num = 1
            else:
                new_num = 1

            new_id = f"RUL-{new_num:04d}"

            new_rule = GajiRule(
                id=new_id,
                id_jabatan_karyawan=validated['id_jabatan_karyawan'],
                formula=validated['formula'],
                variables=validated.get('variables', [])
            )

            db.session.add(new_rule)
            db.session.commit()

            result = gaji_rule_schema.dump(new_rule)
            return jsonify({
                'success': True,
                'message': 'Rule gaji berhasil ditambahkan',
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
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

    @staticmethod
    def update(id):
        """Update gaji rule"""
        try:
            rule = GajiRule.query.get(id)
            if not rule:
                return jsonify({
                    'success': False,
                    'message': 'Rule gaji tidak ditemukan'
                }), 404

            data = request.get_json()
            validated = gaji_rule_update_schema.load(data)

            if 'formula' in validated:
                rule.formula = validated['formula']

            if 'variables' in validated:
                rule.variables = validated['variables']

            db.session.commit()

            result = gaji_rule_schema.dump(rule)
            return jsonify({
                'success': True,
                'message': 'Rule gaji berhasil diupdate',
                'data': result
            }), 200

        except ValidationError as e:
            return jsonify({'success': False, 'errors': e.messages}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

    @staticmethod
    def delete(id):
        """Delete gaji rule"""
        try:
            rule = GajiRule.query.get(id)
            if not rule:
                return jsonify({
                    'success': False,
                    'message': 'Rule gaji tidak ditemukan'
                }), 404

            db.session.delete(rule)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Rule gaji berhasil dihapus'
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
