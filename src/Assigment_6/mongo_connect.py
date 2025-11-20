from pymongo import MongoClient  # type: ignore
from pymongo.errors import ConnectionFailure  # type: ignore


def get_mongo_client():
    uri = "mongodb://mitali:mitali123@localhost:27017/?authSource=admin"
    client = MongoClient(uri)
    return client


if __name__ == "__main__":
    client = get_mongo_client()

    try:
        client.admin.command("ping")
        print("Connected to MongoDB")

    except ConnectionFailure as e:
        print("Connection failed to MongoDB")
        print("Error:", e)
