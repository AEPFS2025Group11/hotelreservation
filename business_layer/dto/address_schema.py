from marshmallow import Schema, fields


class AddressSchema(Schema):
    address_id = fields.Int(dump_only=True)
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    zip_code = fields.Str(required=True)
