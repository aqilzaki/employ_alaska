# app/dto/karyawan_dto.py
from marshmallow import Schema, fields, validate
from app.dto.departemen_dto import DepartemenSchema
from app.dto.jabatan_dto import JabatanSchema
from app.dto.status_pernikahan_dto import StatusPernikahanSchema
from app.dto.status_kerja_dto import StatusKerjaSchema
from app.dto.kondisi_akun_dto import KondisiAkunSchema
from app.dto.agama_dto import AgamaSchema

#
# OUTPUT (dump) schema - include nested relationships (dump_only)
#



class KaryawanSchema(Schema):
    """
    Full serializer for responses (dump). Includes nested relationships (dump_only).
    """
    id = fields.Str(required=True)
    nama = fields.Str(required=True)
    nik = fields.Str(required=True)
    id_status_pernikahan = fields.Str(required=True)
    id_jabatan_karyawan = fields.Str(required=True)
    id_departemen = fields.Str(required=True)
    id_kondisi_akun = fields.Str(required=True)
    id_agama = fields.Str(required=True)
    alamat = fields.Str(required=True)
    npwp = fields.Str(allow_none=True)
    status_pajak = fields.Str(allow_none=True)
    durasi_kontrak = fields.Int(allow_none=True)
    no_hp = fields.Str(required=True)
    tanggal_masuk = fields.Str(required=True)
    awal_kontrak = fields.Date(required=True)
    akhir_kontrak = fields.Date(required=True)
    id_status_kerja_karyawan = fields.Str(required=True)

    # Nested (dump only)
    jabatan = fields.Nested(JabatanSchema, dump_only=True)
    status_pernikahan_rel = fields.Nested(StatusPernikahanSchema, dump_only=True)
    status_kerja = fields.Nested(StatusKerjaSchema, dump_only=True)
    kondisi_akun_rel = fields.Nested(KondisiAkunSchema, dump_only=True)
    agama_rel = fields.Nested(AgamaSchema, dump_only=True)
    departemen_rel = fields.Nested(DepartemenSchema, dump_only=True)

#
# INPUT (load) schemas - only primitive fields; NO nested relationship objects
#
class KaryawanCreateSchema(Schema):
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    nama = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    nik = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    id_status_pernikahan = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    id_jabatan_karyawan = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    id_departemen = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    id_kondisi_akun = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    id_agama = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    alamat = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    npwp = fields.Str(required=False, allow_none=True, validate=validate.Length(max=50))
    status_pajak = fields.Str(required=False, allow_none=True, validate=validate.Length(max=50))
    durasi_kontrak = fields.Int(required=False, allow_none=True)
    no_hp = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    tanggal_masuk = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    awal_kontrak = fields.Date(required=True)
    akhir_kontrak = fields.Date(required=True)
    id_status_kerja_karyawan = fields.Str(required=True, validate=validate.Length(min=1, max=255))

class KaryawanUpdateSchema(Schema):
    # All fields optional for update; still primitives only
    nama = fields.Str(required=False, validate=validate.Length(min=1, max=255))
    nik = fields.Str(required=False, validate=validate.Length(min=1, max=20))
    id_status_pernikahan = fields.Str(required=False, validate=validate.Length(max=255))
    id_jabatan_karyawan = fields.Str(required=False, validate=validate.Length(max=255))
    id_departemen = fields.Str(required=False, validate=validate.Length(max=255))
    id_kondisi_akun = fields.Str(required=False, validate=validate.Length(max=255))
    id_agama = fields.Str(required=False, validate=validate.Length(max=255))
    alamat = fields.Str(required=False, validate=validate.Length(min=1, max=255))
    npwp = fields.Str(required=False, allow_none=True, validate=validate.Length(max=50))
    status_pajak = fields.Str(required=False, allow_none=True, validate=validate.Length(max=50))
    durasi_kontrak = fields.Int(required=False, allow_none=True)
    no_hp = fields.Str(required=False, validate=validate.Length(min=1, max=20))
    tanggal_masuk = fields.Str(required=False, validate=validate.Length(max=255))
    awal_kontrak = fields.Date(required=False)
    akhir_kontrak = fields.Date(required=False)
    id_status_kerja_karyawan = fields.Str(required=False, validate=validate.Length(max=255))


class update_kondisi_akun_schema(Schema):
    id = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    id_kondisi_akun = fields.Str(required=False, validate=validate.Length(max=255))


# Initialize schema instances
karyawan_schema = KaryawanSchema()
karyawan_list_schema = KaryawanSchema(many=True)
karyawan_create_schema = KaryawanCreateSchema()
karyawan_update_schema = KaryawanUpdateSchema()
update_kondisi_akun_schema = update_kondisi_akun_schema()
