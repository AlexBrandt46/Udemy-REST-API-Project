"""_summary_
File contains API requests for stores
"""

import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)

@app.get("/store")  # http://127.0.0.1:5000/store
def get_stores() -> dict:
    """_summary_
    Performs GET request to retrieve all stores
    Returns:
        dict: A dictionary containing a list of all stores
    """
    return { "stores": list(stores.values()) }


@app.post("/store")  # http://127.0.0.1:5000/store
def create_store() -> tuple:
    """_summary_
    Performs POST request to create a new store
    Returns:
        dict: The store that was created as part of this request
        int: The status code of the response
    """
    store_data = request.get_json()
    
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="Store already exists.")
    
    store_id = uuid.uuid4().hex
    store = { **store_data, "id": store_id }  # ** unpacks data in store_data and stores each key-value pair
    stores[store_id] = store
    return store, 201


@app.get("/store/<string:store_id>")
def get_store(store_id) -> tuple:
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")

@app.post("/item")
def create_item():
    """
    Performs POST request to add an item using the store name in the URL
    Returns:
        dict: Response message
        int: The status code of the response
    """
    item_data = request.get_json()  # Grabs the incoming JSON from the request

    if (
        "price" not in item_data or
        "store_id" not in item_data or
        "name" not in item_data
    ):
        abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")

    for item in items.values():
        if (
            item_data["name"] == item["name"] and
            item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="Item already exists.")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = { **item_data, "id": item_id }
    items[item_id] = item

    return item, 201

@app.get("/item")
def get_all_items():
    return { "items": list(items.values()) }

@app.get("/item/<string:item_id>")
def get_item(item_id: str):
    """_summary_
    Performs GET request to retrieve all of the items from a specific store
    Args:
        name (str): The name of the store to retrieve specific items from
    Returns:
        dict: Response message/data
        int: The status code of the response
    """

    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Store not found")
       
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return { "message": "Item deleted." }
    except KeyError:
        abort(404, message="Item not found.")
  
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return { "message": "Store deleted." }
    except KeyError:
        abort(404, message="Store not found.")
       
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.")
        
    try:
        item = items[item_id]
        item |= item_data  # Does an inplace modification to the dictionary that updates the values in item with those in the corresponding keys in item_data
        
        return item
    except KeyError:
        abort(404, message="Item not found.")
        
@app.put("/store/<string:store_id>")
def update_store(store_id):
    store_data = request.get_json()
    
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        
    try:
        store = stores[store_id]
        store |= store_data
        
        return store
    except KeyError:
        abort(404, message="Store not found.")
        