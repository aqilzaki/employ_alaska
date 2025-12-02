from marshmallow import Schema, fields, validate

class TunjanganOpsionalSchema(Schema):
    keterangan = fields.Str(required=True)
    jumlah = fields.Int(required=True)

class PotonganOpsionalSchema(Schema):
    keterangan = fields.Str(required=True)
    jumlah = fields.Int(required=True)

class GajiSettingSchema(Schema):
    id = fields.Str()
    departemen_id = fields.Str()
    jabatan_id = fields.Str()
    status_kerja_id = fields.Str()
    gaji_pokok = fields.Int()
    tunjangan_pokok = fields.Int()
    total_gaji = fields.Int()

    tunjangan_opsional = fields.List(fields.Nested(TunjanganOpsionalSchema))
    potongan_opsional = fields.List(fields.Nested(PotonganOpsionalSchema))

    departemen = fields.Nested('DepartemenSchema', dump_only=True)
    jabatan = fields.Nested('JabatanSchema', dump_only=True)
    status_kerja = fields.Nested('StatusKerjaSchema', dump_only=True)

class GajiSettingCreateSchema(Schema):
    departemen_id = fields.Str(required=True)
    jabatan_id = fields.Str(required=True)
    status_kerja_id = fields.Str(required=True)

    gaji_pokok = fields.Int(required=True)
    tunjangan_pokok = fields.Int(required=True)

    tunjangan_opsional = fields.List(fields.Nested(TunjanganOpsionalSchema), required=False)
    potongan_opsional = fields.List(fields.Nested(PotonganOpsionalSchema), required=False)

class GajiSettingUpdateSchema(Schema):
    gaji_pokok = fields.Int(required=False)
    tunjangan_pokok = fields.Int(required=False)
    tunjangan_opsional = fields.List(fields.Nested(TunjanganOpsionalSchema), required=False)
    potongan_opsional = fields.List(fields.Nested(PotonganOpsionalSchema), required=False)


gaji_setting_schema = GajiSettingSchema()
gaji_setting_list_schema = GajiSettingSchema(many=True)
gaji_setting_create_schema = GajiSettingCreateSchema()
gaji_setting_update_schema = GajiSettingUpdateSchema()
