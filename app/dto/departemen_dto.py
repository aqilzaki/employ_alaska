from marshmallow import Schema, fields, validate

class DepartemenSchema(Schema):
    id = fields.Str(required=True, validate=validate.Length(max=255))
    nama_departemen = fields.Str(required=True, validate=validate.Length(max=100))
    
class DepartemenCreateSchema(Schema):
    nama_departemen = fields.Str(required=True, validate=validate.Length(max=100))
    

class DepartemenUpdateSchema(Schema):
    nama_departemen = fields.Str(required=False, validate=validate.Length(max=100))
    
# Initialize schemas
departemen_schema = DepartemenSchema()
departemen_list_schema = DepartemenSchema(many=True)
departemen_create_schema = DepartemenCreateSchema() 
departemen_update_schema = DepartemenUpdateSchema()

