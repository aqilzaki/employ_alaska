from flask import jsonify, request
from app import db
import uuid
from app.models.gaji_setting import GajiSetting
from app.models.gaji_setting_tunjangan import GajiSettingTunjangan
from app.models.gaji_setting_potongan import GajiSettingPotongan

from app.dto.gaji_setting_dto import (
    gaji_setting_schema,
    gaji_setting_list_schema,
    gaji_setting_create_schema,
    gaji_setting_update_schema
)

from marshmallow import ValidationError


class GajiSettingController:

    @staticmethod
    def get_all():
        data = GajiSetting.query.all()
        return jsonify({
            "success": True,
            "data": gaji_setting_list_schema.dump(data)
        }), 200


    @staticmethod
    def get_by_id(id):
        item = GajiSetting.query.get(id)
        if not item:
            return jsonify({"success": False, "message": "Setting tidak ditemukan"}), 404

        return jsonify({
            "success": True,
            "data": gaji_setting_schema.dump(item)
        }), 200


    @staticmethod
    def create():
        try:
            body = request.json
            validated = gaji_setting_create_schema.load(body)

            new_id = f"GS-{uuid.uuid4().hex[:6]}"

            setting = GajiSetting(
                id=new_id,
                departemen_id=validated["departemen_id"],
                jabatan_id=validated["jabatan_id"],
                status_kerja_id=validated["status_kerja_id"],
                gaji_pokok=validated["gaji_pokok"],
                tunjangan_pokok=validated["tunjangan_pokok"],
            )

            db.session.add(setting)
            db.session.commit()

            # Tunjangan opsional
            tunjangan_items = []
            if "tunjangan_opsional" in validated:
                for item in validated["tunjangan_opsional"]:
                    tun = GajiSettingTunjangan(
                        id=str(uuid.uuid4()),
                        gaji_setting_id=new_id,
                        keterangan=item["keterangan"],
                        jumlah=item["jumlah"]
                    )
                    tunjangan_items.append(tun)
                    db.session.add(tun)

            # Potongan opsional
            potongan_items = []
            if "potongan_opsional" in validated:
                for item in validated["potongan_opsional"]:
                    pot = GajiSettingPotongan(
                        id=str(uuid.uuid4()),
                        gaji_setting_id=new_id,
                        keterangan=item["keterangan"],
                        jumlah=item["jumlah"]
                    )
                    potongan_items.append(pot)
                    db.session.add(pot)

            db.session.commit()

            # Auto calculate total
            total_tunjangan_opsional = sum([t.jumlah for t in tunjangan_items])
            total_potongan_opsional = sum([p.jumlah for p in potongan_items])

            setting.total_tunjangan_opsional = total_tunjangan_opsional
            setting.total_potongan_opsional = total_potongan_opsional
            setting.total_gaji = (
                setting.gaji_pokok +
                setting.tunjangan_pokok +
                total_tunjangan_opsional -
                total_potongan_opsional
            )

            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Setting gaji berhasil dibuat",
                "data": gaji_setting_schema.dump(setting)
            }), 201

        except ValidationError as e:
            return jsonify({"success": False, "errors": e.messages}), 400


    @staticmethod
    def delete(id):
        item = GajiSetting.query.get(id)
        if not item:
            return jsonify({"success": False, "message": "Setting tidak ditemukan"}), 404

        db.session.delete(item)
        db.session.commit()

        return jsonify({"success": True, "message": "Setting berhasil dihapus"}), 200


    @staticmethod
    def hitung(id):
        setting = GajiSetting.query.get(id)

        if not setting:
            return jsonify({"success": False, "message": "Setting tidak ditemukan"}), 404

        total = setting.total_gaji

        return jsonify({
            "success": True,
            "data": {
                "id": id,
                "total_gaji": total
            }
        }), 200
