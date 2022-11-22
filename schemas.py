from marshmallow import Schema, fields


class ListSchema(Schema):
    name = fields.Str()
