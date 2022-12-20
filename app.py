"""_summary_
File contains API requests for stores
"""

from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

@app.get("/store")  # http://127.0.0.1:5000/store
def get_stores() -> dict:
    """_summary_
    Performs GET request to retrieve all stores
    Returns:
        dict: A dictionary containing a list of all stores
    """
    return { "stores": stores }


@app.post("/store")  # http://127.0.0.1:5000/store
def create_store() -> tuple:
    """_summary_
    Performs POST request to create a new store
    Returns:
        dict: The store that was created as part of this request
        int: The status code of the response
    """
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_item(name: str):
    """
    Performs POST request to add an item using the store name in the URL
    Args:
        name (str): The name of the store, we want to add an item to
    Returns:
        dict: Response message
        int: The status code of the response
    """
    request_data = request.get_json()  # Grabs the incoming JSON from the request

    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            store["items"].append(new_item)

            return new_item, 201

    return { "message": "Store not Found" }, 404


@app.get("/store/<string:name>/items")
def get_item(name: str):
    """_summary_
    Performs GET request to retrieve all of the items from a specific store
    Args:
        name (str): The name of the store to retrieve specific items from
    Returns:
        dict: Response message/data
        int: The status code of the response
    """

    for store in stores:
        if store["name"] == name:
            return { "items": store["items"] }, 201

    return { "message": "Store not Found" }, 404