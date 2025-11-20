from mongoengine import connect, Document, EmbeddedDocument  # type: ignore
from mongoengine import StringField, IntField, ListField, EmbeddedDocumentField  # type: ignore
from mongoengine import ValidationError  # type: ignore
from bson import ObjectId  # type: ignore


def init_mongoengine():
    connect(
        db="assignment_db",
        host="mongodb://mitali:mitali123@localhost:27017/assignment_db?authSource=admin",
    )
    print("MongoEngine connected")


class Profile(EmbeddedDocument):
    age = IntField(required=True)
    country = StringField(required=True)
    languages = ListField(StringField(), default=list)


class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True)
    university = StringField()
    course = StringField()
    profile = EmbeddedDocumentField(Profile)


def create_user(username, email, age, country, languages, university, course):
    try:
        profile = Profile(age=age, country=country, languages=languages)

        user = User(
            username=username,
            email=email,
            university=university,
            course=course,
            profile=profile,
        )

        user.save()
        print("User created with id:", user.id)

    except ValidationError as e:
        print("Validation error:", e)
    except Exception as e:
        print("Error:", e)

    create_user(
        username="mitali2",
        email="mitali2@example.com",
        age=33,
        country="Germany",
        languages=["English", "Hindi"],
        university="Constructor University",
        course="Python programming",
    )


def get_user_by_username(username):
    try:
        user = User.objects(username=username).first()

        if user:
            print("User found:")
            print(user.to_mongo().to_dict())
        else:
            print("No user found with that username.")

    except Exception as e:
        print("Error:", e)


def get_users_by_country(country):
    try:
        users = User.objects(profile__country=country)

        print(f"Users from {country}:")
        for user in users:
            print(user.to_mongo().to_dict())

    except Exception as e:
        print("Error:", e)


def update_user_email(username, new_email):
    try:
        result = User.objects(username=username).update_one(set__email=new_email)
        if result > 0:
            print("Email updated successfully.")
        else:
            print("No user found to update.")

    except ValidationError as e:
        print("Validation error:", e)
    except Exception as e:
        print("Error:", e)


def add_language(username, language):
    try:
        result = User.objects(username=username).update_one(push__profile__languages=language)

        if result > 0:
            print("Language added successfully.")
        else:
            print("User not found.")

    except Exception as e:
        print("Error:", e)


def update_course_by_id(object_id, new_course):
    try:
        result = User.objects(id=ObjectId(object_id)).update_one(set__course=new_course)

        if result > 0:
            print("Course updated successfully.")
        else:
            print("No user found with that id.")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    init_mongoengine()

    print("\nFetch by username:")
    get_user_by_username("mitali2")

    print("\nFetch by country:")
    get_users_by_country("Germany")

    print("\nUpdating email:")
    update_user_email("mitali2", "new_email2@example.com")

    print("\nAdding language:")
    add_language("mitali2", "German")

    print("\nUpdating course by ObjectId:")
    update_course_by_id("6919fe63627c93d5bbed72f9", "Advanced Python Programming")

    print("\nVerify updated user:")
    get_user_by_username("mitali2")
