from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from database import users_collection, blog_collection
from routers.auth import get_current_user
from schema.schemas import list_serializer_user
from bson import ObjectId

router = APIRouter(prefix="/api/adminuser", tags=["adminuser"])

user_dependency = Annotated[dict, Depends(get_current_user)]

"""
ADMIN ENDPOINTS
only user with role admin can access these endpoints
"""


@router.get("/all_users", status_code=status.HTTP_200_OK)
async def get_all_users(user: user_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have to be an admin to perform this operation.",
        )

    user_obj = await users_collection.find()
    return list_serializer_user(user_obj)


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_any_user(user: user_dependency, user_id: str):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have to be an admin to perform this operation.",
        )

    deleting_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if deleting_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user to be deleted is not found",
        )

    users_collection.delete_one({"_id": deleting_user["_id"]})
    return {"message": "User deleted successfully"}


@router.delete("/deleteblog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_any_blog(user: user_dependency, blog_id: str):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have to be an admin to perform this operation.",
        )

    blog = await blog_collection.find_one({"_id": ObjectId(blog_id)})

    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found",
        )

    blog_collection.delete_one({"_id": blog["_id"]})
    return {"message": "Blog deleted successfully"}
