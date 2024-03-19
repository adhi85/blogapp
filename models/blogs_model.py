from typing import List
from pydantic import BaseModel, Field

# BlogRequest is a class that will be used to validate the request body when creating a new blog
class BlogRequest(BaseModel):
    title: str = Field(min_length=3)
    body: str = Field(min_length=4, max_length=100)
    tags: List[str] = []
