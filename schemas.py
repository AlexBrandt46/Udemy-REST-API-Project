from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Str(dump_only=True)  # dump_only=True means that we'll only use the id field when it's returned from the API, not sent
    name = fields.Str(required=True)  # required=True means that this field should always be returned by the API
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    
    
class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)