from marshmallow import Schema, fields, validate

class AbsensiSchema(Schema):
    id = fields.Str()
    id_karyawan = fields.Str()
    tanggal = fields.Date()
    jam_in = fields.Time(allow_none=True)
    jam_out = fields.Time(allow_none=True)
    foto_in = fields.Str(allow_none=True)
    foto_out = fields.Str(allow_none=True)


class AbsensiInSchema(Schema):
    foto_in = fields.Raw(required=True,minlength=1)


class AbsensiOutSchema(Schema):
    foto_out = fields.Raw(required=True)


absensi_schema = AbsensiSchema()
absensi_in_schema = AbsensiInSchema()
absensi_out_schema = AbsensiOutSchema()
