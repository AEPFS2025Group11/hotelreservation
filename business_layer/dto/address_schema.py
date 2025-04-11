from marshmallow import Schema, fields


class AddressSchema(Schema):
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    zipcode = fields.Str(required=True)
    id = fields.Int(dump_only=True)
