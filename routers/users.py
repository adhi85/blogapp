from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from models.auth_model import PasswordChange, UpdateUserRequest
from routers.auth import get_current_user
from database import users_collection
from passlib.context import CryptContext
from bson import ObjectId
from schema.schemas import individual_serializer_user, list_serializer_user


router = APIRouter(prefix="/api/users", tags=["users"])

user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
ADMIN ENDPOINTS
only user with role admin can access these endpoints
"""


@router.get("/adminuser/all_users", status_code=status.HTTP_200_OK)
async def get_all_users(user: user_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have to be an admin to perform this operation.",
        )

    user_obj = users_collection.find()
    return list_serializer_user(user_obj)


@router.delete("/adminuser/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency, user_id: str):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have to be an admin to perform this operation.",
        )

    users_collection.delete_one({"_id": ObjectId(user_id)})
    return {"message": "User deleted successfully"}


"""
USER ENDPOINTS
all users can access these endpoints
"""


@router.get("/info", status_code=status.HTTP_200_OK)
async def get_current_user_info(user: user_dependency):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    user_obj = individual_serializer_user(
        users_collection.find_one({"username": user.get("username")})
    )

    return user_obj


# Change password endpoint for the user to change their password
@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, user_verification: PasswordChange):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    user_obj = users_collection.find_one({"username": user.get("username")})

    if not bcrypt_context.verify(user_verification.password, user_obj["password"]):
        raise HTTPException(status_code=401, detail="Current Password is wrong")

    user_obj["password"] = bcrypt_context.hash(user_verification.new_password)

    users_collection.find_one_and_replace({"username": user.get("username")}, user_obj)


# update_user_info is a route that will update the user's information in the database
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_info(user: user_dependency, user_verification: UpdateUserRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    users_collection.find_one_and_update(
        {"_id": ObjectId(user.get("id"))}, {"$set": dict(user_verification)}
    )
    return {"message": "User updated successfully"}


# add_tags_to_user is a route that will add tags to the user's profile
@router.put("/add_tags/", status_code=status.HTTP_204_NO_CONTENT)
async def add_tags_to_user(user: user_dependency, tags: List[str]):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    users_collection.update_one(
        {"_id": ObjectId(user.get("id"))}, {"$addToSet": {"tags": {"$each": tags}}}
    )
    return {"message": "Tags added successfully"}


# remove_tags_from_user is a route that will remove tags from the user's profile
@router.put("/remove_tags/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tags_from_user(user: user_dependency, tags: List[str]):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    users_collection.update_one(
        {"_id": ObjectId(user.get("id"))}, {"$pullAll": {"tags": tags}}
    )

    return {"message": "Tags removed successfully"}
