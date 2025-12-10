

from marshmallow import Schema, fields, validate

class StatusKerjaSchema(Schema):
    id = fields.Str(required=True, validate=validate.Length(max=255))
    nama_status = fields.Str(required=True, validate=validate.Length(max=255))

class StatusKerjaCreateSchema(Schema):
    nama_status = fields.Str(required=True, validate=validate.Length(min=1, max=255))

class StatusKerjaUpdateSchema(Schema):
    nama_status = fields.Str(required=False, validate=validate.Length(min=1, max=255))

# Initialize schemas
status_kerja_schema = StatusKerjaSchema()
status_kerja_list_schema = StatusKerjaSchema(many=True)
status_kerja_create_schema = StatusKerjaCreateSchema()
status_kerja_update_schema = StatusKerjaUpdateSchema()