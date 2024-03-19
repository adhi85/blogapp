from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from models.auth_model import CreateUserRequest, Token
from passlib.context import CryptContext
from database import users_collection
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# bcrypt_context is an instance of CryptContext that will be used to hash the password
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_bearer is an instance of OAuth2PasswordBearer that will be used to authenticate the user
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


# get_current_user is a dependency that will be used to authenticate the user
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


# create_user will create a new user in the database
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):

    valid_roles = {"admin", "user"}

    if create_user_request.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be either 'admin' or 'user'",
        )

    user_obj = dict(create_user_request)

    if users_collection.find_one({"username": user_obj["username"]}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    if users_collection.find_one({"email": user_obj["email"]}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    hashed_password = bcrypt_context.hash(user_obj["password"])
    user_obj["password"] = hashed_password

    users_collection.insert_one(user_obj)

    return {"message": "User created successfully"}


# authenticate_user will authenticate the user using the username and password
def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user:
        return False
    if not bcrypt_context.verify(password, user["password"]):
        return False

    return user


# create_access_token will create a new access token for the user
def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# login_for_access_token will return the access token for the user
# OAuth2PasswordRequestForm is a form that will be used to get the username and password
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # async def login_for_access_token(form_data: LoginRequest):

    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token(
        user["username"], str(user["_id"]), user["role"], timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}
