from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from bson.objectid import ObjectId
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
def register(user: CreateUserModel):
    check_obj(user)
    if(db.users.find_one({"email": user.email})):
        raise HTTPException(
            status_code=409, detail="{email} already in use".format(email=user.email))
    db_user = user.dict()
    db_user['password'] = get_password_hash(db_user.pop('password'))
    try:
        db.users.insert_one(db_user)
        return "user {email} created".format(email=db_user["email"])
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = authenticate_user(
        db, form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/")
def update_profile(user: UpdateUserModel, token: str = Depends(oauth2_scheme)):
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


@router.get("/me")
def get_user_info(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    user = db.users.find_one({"email": payload["sub"]})
    user.pop('_id')
    user.pop('password')
    return user


@router.get("/")
def get_users_list(token: str = Depends(oauth2_scheme), practice_id: str = None):
    if practice_id:
        practice = db.practices.find_one({"_id": ObjectId(practice_id)})
        users = []
        for author in practice["authors"]:
            user = db.users.find_one({"_id": ObjectId(author["user_id"])})
            if user is None:
                user = {
                    "name": author["author_name"]
                }
            else:
                user["id"] = str(user.pop("_id"))
            users.append(user)
        return users
        
    users = []
    for user in db.users.find():
        user["id"] = str(user.pop("_id"))
        users.append(user)

    return users

@router.get("/notifications")
def get_user_notifications(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    user = db.users.find_one({"email": payload["sub"]})
    notifications = []
    for notif in db.notifications.find({"user_id": user["_id"]}):
        for key in notif.keys():
            if type(notif[key]) is ObjectId:
                notif[key] = str(notif[key])
        print(notif)
        notifications.append(notif)
    return notifications
        


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


@router.put("/follow")
def follow_user(user_id: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    try:
        user = db.users.find_one({"email": payload["sub"]})
        db.users.find_one_and_update(
            {"_id": ObjectId(user_id)}, {"$push": {"followers": user["_id"]}})
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


@router.get("/img")
def get_profile_photo(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=401, detail="User not found")
    return user["photo"]
