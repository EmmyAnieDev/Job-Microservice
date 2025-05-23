from marshmallow import Schema, fields

class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    company = fields.Str(required=True)
    location = fields.Str(required=True)
    salary = fields.Float()
    date_created = fields.DateTime(dump_only=True)
    date_updated = fields.DateTime(dump_only=True)
