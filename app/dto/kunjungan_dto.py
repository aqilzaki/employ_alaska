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

from marshmallow import Schema, fields

class KunjunganFotoSchema(Schema):
    id = fields.Int()
    foto = fields.Str()
    latitude = fields.Str()
    longitude = fields.Str()
    jam = fields.Time()


class ReportKunjunganSchema(Schema):
    id = fields.Int()
    tanggal = fields.Date()

    # Karyawan
    id_karyawan = fields.Str(attribute="karyawan.id")
    nama_karyawan = fields.Str(attribute="karyawan.nama")

    # Departemen & Jabatan
    departemen = fields.Str(attribute="karyawan.departemen.nama_departemen")
    jabatan = fields.Str(attribute="karyawan.jabatan.nama_jabatan")

    fotos = fields.Nested(KunjunganFotoSchema, many=True)


report_kunjungan_schema = ReportKunjunganSchema()
kunjungan_foto_create_schema = KunjunganFotoCreateSchema()
kunjungan_schema = KunjunganSchema()
