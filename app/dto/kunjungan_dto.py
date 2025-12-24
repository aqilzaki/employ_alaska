from marshmallow import Schema, fields

class KunjunganFotoCreateSchema(Schema):
    foto = fields.Raw(required=True)      # FILE
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)


class KunjunganFotoSchema(Schema):
    id = fields.Int()
    foto = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    jam = fields.Time()


class KunjunganSchema(Schema):
    id = fields.Int()
    id_karyawan = fields.Str()
    tanggal = fields.Date()
    fotos = fields.List(fields.Nested(KunjunganFotoSchema))


kunjungan_foto_create_schema = KunjunganFotoCreateSchema()
kunjungan_schema = KunjunganSchema()
