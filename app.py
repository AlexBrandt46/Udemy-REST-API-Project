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
