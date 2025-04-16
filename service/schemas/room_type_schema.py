from marshmallow import Schema, fields


class RoomSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(dump_only=True)
    max_guests = fields.Int(dump_only=True)
