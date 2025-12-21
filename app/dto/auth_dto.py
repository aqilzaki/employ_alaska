from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    id = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=20),
        error_messages={"required": "ID wajib diisi"}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        error_messages={"required": "Password wajib diisi"}
    )


class RefreshSchema(Schema):
    pass  # tidak butuh body


class LogoutSchema(Schema):
    pass


refresh_schema = RefreshSchema()
logout_schema = LogoutSchema()
login_schema = LoginSchema()
