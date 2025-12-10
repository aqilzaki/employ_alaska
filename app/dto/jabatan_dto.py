

from marshmallow import Schema, fields, validate

class JabatanSchema(Schema):
    id = fields.Str(required=True, validate=validate.Length(max=255))
    nama_jabatan = fields.Str(required=True, validate=validate.Length(max=255))

class JabatanCreateSchema(Schema):
    nama_jabatan = fields.Str(required=True, validate=validate.Length(min=1, max=255))

class JabatanUpdateSchema(Schema):
    nama_jabatan = fields.Str(required=False, validate=validate.Length(min=1, max=255))

# Initialize schemas
jabatan_schema = JabatanSchema()
jabatan_list_schema = JabatanSchema(many=True)
jabatan_create_schema = JabatanCreateSchema()
jabatan_update_schema = JabatanUpdateSchema()