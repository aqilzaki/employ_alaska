from marshmallow import Schema, fields, validate

class StatusPernikahanSchema(Schema):
    id = fields.Str(required=True, validate=validate.Length(max=255))
    nama_status_pernikahan = fields.Str(required=True, validate=validate.Length(max=255))

class StatusPernikahanCreateSchema(Schema):
    nama_status_pernikahan = fields.Str(required=True, validate=validate.Length(min=1, max=255))  

class StatusPernikahanUpdateSchema(Schema):
    nama_status_pernikahan = fields.Str(required=False, validate=validate.Length(min=1, max=255))

# Initialize schemas
status_pernikahan_schema = StatusPernikahanSchema()
status_pernikahan_list_schema = StatusPernikahanSchema(many=True)
status_pernikahan_create_schema = StatusPernikahanCreateSchema()
status_pernikahan_update_schema = StatusPernikahanUpdateSchema()
