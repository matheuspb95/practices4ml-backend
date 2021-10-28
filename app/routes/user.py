from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.db.connection import db
from app.models.models import CreateUserModel, Token, UpdateUserModel
from app.controllers.validations import check_obj
from app.controllers.security import get_password_hash, authenticate_user, decode_token
import re

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_user(user: CreateUserModel):
    check_obj(user)
    if(db.users.find_one({"email": user.email})):
        raise HTTPException(
            status_code=409, detail="{email} already in use".format(email=user.email))
    db_user = user.dict()
    db_user['password'] = get_password_hash(db_user.pop('password'))
    try:
        db.users.insert_one(db_user)
        return "user {email} created".format(email=db_user["email"])
    except:
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = authenticate_user(
        db, form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/")
def update_user(user: UpdateUserModel, token: str = Depends(oauth2_scheme)):
    check_obj(user)
    payload = decode_token(token)
    if (not db.users.find_one({"email": payload["sub"]})):
        raise HTTPException(
            status_code=401, detail="User not authenticated")
    result = db.users.update_one({"email": user.email}, {"$set": user.dict()})
    if (not result.modified_count):
        raise HTTPException(
            status_code=400, detail="No user found or modified")
    return "User {} saved".format(user.email)


@router.get("/")
def get_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    user = db.users.find_one({"email": payload["sub"]})
    user.pop('_id')
    user.pop('password')
    return user


@router.get("/search")
def search_user(search: str):
    regex = re.compile("^{search}".format(search=search), flags=re.IGNORECASE)
    find = db.users.find({"name": {"$regex": regex}}, {
        "_id": 1, "name": 1})
    res = []
    for user in find:
        user["user_id"] = str(user.pop("_id"))
        user["author_name"] = user["name"]
        res.append(user)
    return res
