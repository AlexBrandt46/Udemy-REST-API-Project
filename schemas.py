from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    """Item schema that's used only for representing an item with no relationship to a store

    Args:
        Schema: PlainItemSchema is a subclass of Schema
    """
    id = fields.Str(dump_only=True)  # dump_only=True means that we'll only use the id field when it's returned from the API, not sent
    name = fields.Str(required=True)  # required=True means that this field should always be returned by the API
    price = fields.Float(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class PlainStoreSchema(Schema):
    """Store schema that's used only for representing a store with no relationship to any items

    Args:
        Schema: PlainStoreSchema is a subclass of Schema
    """
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    """Item schema that's used to represent an item along with its relationship to a store
        A subclass was created, so there wasn't a recursive nesting relationship made between ItemSchema and StoreSchema since they would become dependent on each other
    Args:
        PlainItemSchema: ItemSchema is a subclass of PlainItemSchema
    """
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    """Store schema that's used to represent a store along with its relationship to items
        A subclass was created, so there wasn't a recursive nesting relationship made between ItemSchema and StoreSchema since they would become dependent on each other
    Args:
        PlainStoreSchema: StoreSchema is a subclass of PlainStoreSchema
    """
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
