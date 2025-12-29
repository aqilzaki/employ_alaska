from marshmallow import Schema, fields
from app.dto.status_request_dto import StatusSchema

class IzinSchema(Schema):
    id = fields.Int()
    id_karyawan = fields.Str()
    tanggal = fields.Date()
    jam = fields.Time()
    foto = fields.Str()
    keterangan = fields.Str()
    status = fields.Nested(lambda: StatusSchema)
    approved_by = fields.Str(allow_none=True)
    created_at = fields.DateTime()



izin_schema = IzinSchema()
izin_list_schema = IzinSchema(many=True)
