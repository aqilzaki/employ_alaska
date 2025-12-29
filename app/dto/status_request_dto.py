from marshmallow import Schema, fields

class StatusSchema(Schema):
    id = fields.Int()
    kode = fields.Str()
    nama = fields.Str()
