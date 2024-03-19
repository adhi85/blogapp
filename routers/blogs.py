from datetime import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from database import blog_collection
from schema.schemas import individual_serializer_blog, list_serializer
from bson import ObjectId
from models.blogs_model import BlogRequest
from .auth import get_current_user

router = APIRouter(prefix="/blogs", tags=["blogs"])

user_dependency = Annotated[dict, Depends(get_current_user)]


# read_all is a route that will return all the blogs in the database
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc",
):
    # Define default values for sorting
    sort_direction = -1 if sort_order == "desc" else 1

    # Sort by the specified field if provided
    blogs = list_serializer(blog_collection.find().sort(sort_by, sort_direction))

    # Apply pagination
    blogs = blogs[offset : offset + limit]

    return blogs


# read_my_blogs is a route that will return all the blogs that belong to the authenticated user
@router.get("/myblogs", status_code=status.HTTP_200_OK)
async def read_my_blogs(
    user: user_dependency,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    sort_by: Optional[str] = "updated_at",
    sort_order: Optional[str] = "desc",
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    sort_direction = -1 if sort_order == "desc" else 1

    blogs = list_serializer(
        blog_collection.find({"owner_id": user.get("id")}).sort(sort_by, sort_direction)
    )

    # Apply pagination
    blogs = blogs[offset : offset + limit]

    return blogs


# Read a single blog by its ID
@router.get("/{blog_id}", status_code=status.HTTP_200_OK)
async def read_blog(blog_id: str):
    try:
        blog = individual_serializer_blog(
            blog_collection.find_one({"_id": ObjectId(blog_id)})
        )
        return blog
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog not found"
        )


# create_blog is a route that will create a new blog in the database
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_blog(user: user_dependency, blog_request: BlogRequest):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    blog = dict(blog_request)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blog["owner_id"] = user.get("id")
    blog["created_at"] = current_time
    blog["updated_at"] = current_time
    blog_collection.insert_one(blog)

    return {"message": "Blog created successfully"}


# update_blog is a route that will update a blog in the database
@router.put("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_blog(user: user_dependency, blog_request: BlogRequest, blog_id: str):

    try:
        blog = blog_collection.find_one({"_id": ObjectId(blog_id)})

        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog not found"
            )

        if user is None or blog["owner_id"] != user.get("id"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        updated_blog_data = dict(blog_request)
        updated_blog_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        blog_collection.find_one_and_update(
            {"_id": ObjectId(blog_id)}, {"$set": dict(updated_blog_data)}
        )

        return {"message": "Blog updated successfully"}
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog not found"
        )


# delete_blog is a route that will delete a blog from the database
@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(user: user_dependency, blog_id: str):

    try:
        blog = blog_collection.find_one({"_id": ObjectId(blog_id)})
        if user is None or blog["owner_id"] != user.get("id"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        blog_collection.find_one_and_delete({"_id": ObjectId(blog_id)})
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog not found"
        )

    return {"message": "Blog deleted successfully"}
