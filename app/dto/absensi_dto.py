from marshmallow import Schema, fields, validate

class AbsensiSchema(Schema):
    id = fields.Str()
    id_karyawan = fields.Str()
    tanggal = fields.Date()
    jam_in = fields.Time(allow_none=True)
    jam_out = fields.Time(allow_none=True)
    foto_in = fields.Str(allow_none=True)
    foto_out = fields.Str(allow_none=True)
    longitude_in = fields.Float(allow_none=True)
    latitude_in = fields.Float(allow_none=True)
    longitude_out = fields.Float(allow_none=True)
    latitude_out = fields.Float(allow_none=True)

# =====================
# ABSENSI REPORT (JOIN)
# =====================
class ReportAbsensiSchema(Schema):
    id = fields.Str()
    tanggal = fields.Date()

    jam_in = fields.Time(allow_none=True)
    jam_out = fields.Time(allow_none=True)

    foto_in = fields.Str(allow_none=True)
    foto_out = fields.Str(allow_none=True)

    longitude_in = fields.Float(allow_none=True)
    latitude_in = fields.Float(allow_none=True)
    longitude_out = fields.Float(allow_none=True)
    latitude_out = fields.Float(allow_none=True)

    # ===== KARYAWAN =====
    id_karyawan = fields.Str(attribute="karyawan.id")
    nama_karyawan = fields.Str(attribute="karyawan.nama")

    # ===== DEPARTEMEN =====
    id_departemen = fields.Str(attribute="karyawan.departemen.id")
    nama_departemen = fields.Str(attribute="karyawan.departemen.nama_departemen")

    # ===== JABATAN =====
    id_jabatan = fields.Str(attribute="karyawan.jabatan.id")
    nama_jabatan = fields.Str(attribute="karyawan.jabatan.nama_jabatan")


class AbsensiInSchema(Schema):
    foto_in = fields.Raw(required=True,minlength=1)
    longitude_in = fields.Float(allow_none=True)
    latitude_in = fields.Float(allow_none=True)
 

class AbsensiOutSchema(Schema):
    foto_out = fields.Raw(required=True)
    longitude_out = fields.Float(allow_none=True)
    latitude_out = fields.Float(allow_none=True)


absensi_schema = AbsensiSchema()
absensi_in_schema = AbsensiInSchema()
absensi_out_schema = AbsensiOutSchema()
AbsensiReportSchema = ReportAbsensiSchema()
