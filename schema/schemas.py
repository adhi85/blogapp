from bson import ObjectId
from database import users_collection


# individual_serializer will take a single blog and return a dictionary with the blog details
def individual_serializer_blog(blog) -> dict:
    user = users_collection.find_one({"_id": ObjectId(blog["owner_id"])})
    return {
        "id": str(blog["_id"]),
        "title": blog["title"],
        "body": blog["body"],
        "created_at": blog["created_at"],
        "updated_at": blog["updated_at"],
        "tags": blog["tags"],
        "owner": user["username"],
    }


def list_serializer(blogs) -> list:
    return [individual_serializer_blog(blog) for blog in blogs]


def individual_serializer_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "role": user["role"],
        "tags": user["tags"],
    }


def list_serializer_user(users) -> list:
    return [individual_serializer_user(user) for user in users]
