from marshmallow import Schema, fields, validate

class KondisiAkunSchema(Schema):
    id = fields.Str(required=True)
    nama_kondisi_akun = fields.Str(required=True)

class KondisiAkunCreateSchema(Schema):
    nama_kondisi_akun = fields.Str(required=True, validate=validate.Length(min=1, max=255))

class KondisiAkunUpdateSchema(Schema):
    nama_kondisi_akun = fields.Str(required=False, validate=validate.Length(min=1, max=255))

# Initialize schemas
kondisi_akun_schema = KondisiAkunSchema()
kondisi_akun_list_schema = KondisiAkunSchema(many=True)
kondisi_akun_create_schema = KondisiAkunCreateSchema()
kondisi_akun_update_schema = KondisiAkunUpdateSchema()
