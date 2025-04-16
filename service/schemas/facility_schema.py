from marshmallow import Schema, fields


class RoomSchema(Schema):
    id = fields.Int(dump_only=True)
    facility_name = fields.Str(dump_only=True)
