from marshmallow import Schema, fields


class RoomSchema(Schema):
    id = fields.Int(dump_only=True)
    hotel_id = fields.Int(dump_only=True)
    room_number = fields.Str(dump_only=True)
    type_id = fields.Int(required=True)
    price_per_night = fields.Int(required=True)
