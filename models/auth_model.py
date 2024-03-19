from typing import List
from pydantic import BaseModel, EmailStr, Field, validator


# validate_password is a function that will be used to validate the password
def validate_password(cls, v):
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(c.isupper() for c in v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(c.islower() for c in v):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(c.isdigit() for c in v):
        raise ValueError("Password must contain at least one digit")
    return v


# CreateUserRequest is a class that will be used to validate the request body when creating a new user
class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(min_length=8, max_length=50)
    role: str = Field(default="user", description="User role, either 'admin' or 'user'")
    tags: List[str] = []

    @validator("password")
    def password_validation(cls, v):
        return validate_password(cls, v)

class LoginRequest(BaseModel):
    username: str
    password: str

# UpdateUserRequest is a class that will be used to validate the request body when updating a user
class UpdateUserRequest(BaseModel):
    first_name: str
    last_name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordChange(BaseModel):
    password: str
    new_password: str = Field(min_length=8, max_length=50)

    @validator("new_password")
    def password_validation(cls, v):
        return validate_password(cls, v)

    @validator("new_password")
    def password_not_same_as_old(cls, v, values, **kwargs):
        old_password = values.get("password")
        if v == old_password:
            raise ValueError("New password must be different from the old password")
        return v
