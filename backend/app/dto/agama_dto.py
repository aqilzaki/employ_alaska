from marshmallow import Schema, fields, validate

class AgamaSchema(Schema):
    id = fields.Str(required=True, validate=validate.Length(max=255))
    nama_agama = fields.Str(required=True, validate=validate.Length(max=255))

class AgamaCreateSchema(Schema):
    nama_agama = fields.Str(required=True, validate=validate.Length(min=1, max=255))

class AgamaUpdateSchema(Schema):
    nama_agama = fields.Str(required=False, validate=validate.Length(min=1, max=255))

# Initialize schemas
agama_schema = AgamaSchema()
agama_list_schema = AgamaSchema(many=True)
agama_create_schema = AgamaCreateSchema()
agama_update_schema = AgamaUpdateSchema()
