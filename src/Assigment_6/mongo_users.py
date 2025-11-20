from pymongo import MongoClient  # type: ignore
from bson import ObjectId  # type: ignore


def get_mongo_client():
    uri = "mongodb://mitali:mitali123@localhost:27017/?authSource=admin"
    client = MongoClient(uri)
    return client


def create_user(username, email, age, country, languages, university, course):
    client = get_mongo_client()
    db = client["assignment_db"]
    users = db["users"]

    user_document = {
        "username": username,
        "email": email,
        "profile": {"age": age, "country": country, "languages": languages},
        "university": university,
        "course": course,
    }

    result = users.insert_one(user_document)
    print("User created with _id:", result.inserted_id)


if __name__ == "__main__":
    create_user(
        username="mitali",
        email="mitali@gmail.com",
        age=32,
        country="Germany",
        languages=["English", "Hindi"],
        university="Constructor University",
        course="Python programming",
    )


def get_user_by_username(username):
    client = get_mongo_client()
    db = client["assignment_db"]
    users = db["users"]

    user = users.find_one({"username": username})

    if user:
        print("User found:")
        print(user)
    else:
        print("No user found with username:", username)


def get_users_by_country(country):
    client = get_mongo_client()
    db = client["assignment_db"]
    users = db["users"]

    cursor = users.find({"profile.country": country})

    print("Users from", country, ":")

    for user in cursor:
        print(user)


def update_user_email(username, new_email):
    client = get_mongo_client()
    db = client["assignment_db"]
    users = db["users"]

    result = users.update_one({"username": username}, {"$set": {"email": new_email}})

    if result.modified_count > 0:
        print("Email updated successfully.")
    else:
        print("No user updated. Check username.")


def add_language(username, language):
    client = get_mongo_client()
    db = client["assignment_db"]
    users = db["users"]

    result = users.update_one({"username": username}, {"$push": {"profile.languages": language}})

    if result.modified_count > 0:
        print("Language added successfully.")
    else:
        print("No user updated. Check username.")


def update_by_id(object_id, new_course):
    client = get_mongo_client()
    db = client["assignment_db"]
    users = db["users"]

    result = users.update_one(
        {"_id": ObjectId(object_id)},  # converting string to ObjectId
        {"$set": {"course": new_course}},
    )

    if result.modified_count > 0:
        print("Course updated successfully.")
    else:
        print("No document updated. Check ObjectId.")


if __name__ == "__main__":
    print("Fetching by username:")
    get_user_by_username("mitali")

    print("\nFetching by country:")
    get_users_by_country("Germany")

    print("Updating email:")
    update_user_email("mitali", "new_email@example.com")

    print("Adding language:")
    add_language("mitali", "German")

    print("Updating by ObjectId:")
    update_by_id("691917ceede03b8a44d133ff", "Advanced Python")
