""" File containing each of the schemas used in the API calls to serialize data """

from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    """Item schema that's used only for representing an item with no relationship to a store

    Args:
        Schema: PlainItemSchema is a subclass of Schema
    """

    # dump_only=True means we'll only use the id field when it's returned from the API, not sent
    # required=True means that this field should always be returned by the API

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class ItemUpdateSchema(Schema):
    """Item schema that's used to represent an item that will be updated with only editable fields

    Args:
        Schema: PlainItemSchema is a subclass of Schema
    """
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class PlainStoreSchema(Schema):
    """Store schema that's used only for representing a store with no relationship to any items

    Args:
        Schema: PlainStoreSchema is a subclass of Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    """Item schema that's used to represent an item along with its relationship to a store
        A subclass is created, so there's not a recursive nesting relationship made between
        ItemSchema and StoreSchema since they would become dependent on each other
    Args:
        PlainItemSchema: ItemSchema is a subclass of PlainItemSchema
    """
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    """ Store schema that's used to represent a store along with its relationship to items
        A subclass is created, so there's not a recursive nesting relationship made between
        ItemSchema and StoreSchema since they'd become dependent on each other
    Args:
        PlainStoreSchema: StoreSchema is a subclass of PlainStoreSchema
    """
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    """ Schema that represents tags in the DB """
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    """ User schema that represents the users """
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
