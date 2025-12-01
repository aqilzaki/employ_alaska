from marshmallow import Schema, fields, validate

class GajiRuleSchema(Schema):
    id = fields.Str(required=True, validate=validate.Length(max=255))
    id_jabatan_karyawan = fields.Str(required=True, validate=validate.Length(max=255))
    formula = fields.Str(required=True)
    variables = fields.List(fields.Str(), required=False)

class GajiRuleCreateSchema(Schema):
    id_jabatan_karyawan = fields.Str(required=True, validate=validate.Length(max=255))
    formula = fields.Str(required=True)
    variables = fields.List(fields.Str(), required=False)

class GajiRuleUpdateSchema(Schema):
    formula = fields.Str(required=False)
    variables = fields.List(fields.Str(), required=False)

# Initialize schemas
gaji_rule_schema = GajiRuleSchema()
gaji_rule_list_schema = GajiRuleSchema(many=True)
gaji_rule_create_schema = GajiRuleCreateSchema()
gaji_rule_update_schema = GajiRuleUpdateSchema()
