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

            # ==========================
            # GENERATE ID Gaji Setting
            # ==========================
            last = GajiSetting.query.order_by(GajiSetting.id.desc()).first()

            if last:
                try:
                    last_num = int(last.id.split('-')[-1])
                    new_num = last_num + 1
                except:
                    new_num = 1
            else:
                new_num = 1

            setting_id = f"GJ-SET-{new_num:04d}"

            # ==========================
            # CREATE GajiSetting
            # ==========================
            setting = GajiSetting(
                id=setting_id,
                departemen_id=validated["departemen_id"],
                jabatan_id=validated["jabatan_id"],
                status_kerja_id=validated["status_kerja_id"],
                gaji_pokok=validated["gaji_pokok"],
                tunjangan_pokok=validated["tunjangan_pokok"],
            
            )

            db.session.add(setting)
            db.session.commit()

            # Prepare lists
            tunjangan_items = []
            potongan_items = []

            # ==========================
            # TUNJANGAN OPSIONAL
            # ==========================
            if "tunjangan_opsional" in validated:
                for item in validated["tunjangan_opsional"]:

                    # generate tunjangan id
                    tunj_last = GajiSettingTunjangan.query.order_by(
                        GajiSettingTunjangan.id.desc()
                    ).first()

                    if tunj_last:
                        try:
                            last_num = int(tunj_last.id.split('-')[-1])
                            new_num = last_num + 1
                        except:
                            new_num = 1
                    else:
                        new_num = 1

                    tunjangan_id = f"GJ-TNJ-{new_num:04d}"

                    tun = GajiSettingTunjangan(
                        id=tunjangan_id,
                        gaji_setting_id=setting_id,
                        keterangan=item["keterangan"],
                        jumlah=item["jumlah"]
                    )
                    tunjangan_items.append(tun)
                    db.session.add(tun)

            # ==========================
            # POTONGAN OPSIONAL
            # ==========================
            if "potongan_opsional" in validated:
                for item in validated["potongan_opsional"]:

                    pot_last = GajiSettingPotongan.query.order_by(
                        GajiSettingPotongan.id.desc()
                    ).first()

                    if pot_last:
                        try:
                            last_num = int(pot_last.id.split('-')[-1])
                            new_num = last_num + 1
                        except:
                            new_num = 1
                    else:
                        new_num = 1

                    pot_id = f"GJ-PTN-{new_num:04d}"

                    pot = GajiSettingPotongan(
                        id=pot_id,
                        gaji_setting_id=setting_id,
                        keterangan=item["keterangan"],
                        jumlah=item["jumlah"]
                    )
                    potongan_items.append(pot)
                    db.session.add(pot)

            db.session.commit()

            # ==========================
            # AUTO CALCULATE TOTAL
            # ==========================
            total_tunjangan = sum([t.jumlah for t in tunjangan_items])
            total_potongan = sum([p.jumlah for p in potongan_items])

            setting.total_tunjangan_opsional = total_tunjangan
            setting.total_potongan_opsional = total_potongan
            setting.total_gaji = (
                setting.gaji_pokok +
                setting.tunjangan_pokok +
                total_tunjangan -
                total_potongan
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
