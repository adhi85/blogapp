from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from schema.schemas import list_serializer
from routers.auth import get_current_user
from database import blog_collection, users_collection

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
user_dependency = Annotated[dict, Depends(get_current_user)]

"""
    This route will return the blogs that match the tags of the user.
    The user is authenticated using the user_dependency.
    sort_by and sort_order are optional query parameters that will be used to sort the blogs.
    by default, the blogs will be sorted by created_at in descending order so that the latest blogs will be returned first.
"""


@router.get("/blogs", status_code=status.HTTP_200_OK)
async def get_blogs_matching_users_tags(
    user: user_dependency,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc",
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )

    sort_direction = -1 if sort_order == "desc" else 1

    user_tags = users_collection.find_one({"username": user.get("username")})["tags"]

    blogs_matching_tags = list_serializer(
        blog_collection.find({"tags": {"$in": user_tags}}).sort(sort_by, sort_direction)
    )

    blogs_matching_tags = blogs_matching_tags[offset : offset + limit]

    return blogs_matching_tags


@router.get("/blogs/{tag}", status_code=status.HTTP_200_OK)
async def get_all_blogs_with_tag(
    tag: str,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc",
):
    sort_direction = -1 if sort_order == "desc" else 1

    blogs_with_tags = list_serializer(
        blog_collection.find({"tags": tag}).sort(sort_by, sort_direction)
    )

    blogs_with_tags = blogs_with_tags[offset : offset + limit]

    return blogs_with_tags
