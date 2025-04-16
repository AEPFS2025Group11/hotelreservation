from marshmallow import Schema, fields


class HotelSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    stars = fields.Int(required=True)
    address_id = fields.Int(required=True)
