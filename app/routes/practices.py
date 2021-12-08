from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from bson.objectid import ObjectId
from app.db.connection import db
from app.models.models import CreatePractices, UpdatePractices
from app.controllers.security import decode_token
from typing import List
import re

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/practices",
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_practice(practice: CreatePractices, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user = db.users.find_one({"email": payload["sub"]})
        for author in practice.authors:
            if (author.user_id and not db.users.find_one({"_id": ObjectId(author.user_id)})):
                raise HTTPException(
                    status_code=401, detail="Author id not existent")
        practice.create_date = datetime.now()
        result = db.practices.insert_one(practice.dict())

        # for author in practice.authors:
        #     if author.user_id:
        #         notification = {
        #             "user_id": author.user_id,
        #             "type": "added_author",
        #             "text": "User {username} added you as author of practice {practice}!"
        #             .format(username=user["name"], practice=practice.name),
        #             "practice_id": result.inserted_id,
        #             "insert_id": user["_id"],
        #             "read": False,
        #             "date": datetime.now()
        #         }
        #     db.notifications.insert_one(notification)

        return "practice created {id}".format(id=result.inserted_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


@router.get("/")
def get_practices(
        author_id: str = None,
        practice_id: str = None,
        search: str = '',
        skip: int = 0,
        limit: int = 0,
        token: str = Depends(oauth2_scheme)):
    if practice_id:
        return view_practice(practice_id, token)
    else:
        return list_practices(author_id, search, skip, limit, token)


def list_practices(author_id: str = None,
                   search: str = '',
                   skip: int = 0,
                   limit: int = 0,
                   token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    practices = []
    regex = re.compile("^{search}".format(search=search), flags=re.IGNORECASE)
    try:
        user = db.users.find_one({"email": payload["sub"]})
        for prat in db.practices.find({"name": {"$regex": regex}}).skip(skip).limit(limit):
            editable = False
            prat["id"] = str(prat.pop("_id"))
            can_add = False
            for author in prat["authors"]:
                if author["user_id"]:
                    if author["user_id"] == user["_id"]:
                        editable = "editor" in author and author["editor"]
                    author_photo = db.users.find_one(
                        {"_id": author["user_id"]}, ["photo"])
                    author_photo.pop("_id")
                    author["user_id"] = str(author["user_id"])
                    if "photo" in author_photo:
                        author["photo"] = author_photo["photo"]
                if author_id:
                    if author["user_id"] == author_id:
                        can_add = True
                else:
                    can_add = True
            prat["editable"] = editable
            if can_add:
                practices.append(prat)
        practices.reverse()
        return practices
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


def get_comments(practice_id: str, user_id: str):
    comments = []
    for comm in db.comments.find({"practice_id": ObjectId(practice_id)}):
        comm["responses"] = []
        for resp in db.comments.find({"comment_id": comm["_id"]}):
            resp["id"] = str(resp.pop("_id"))
            resp["comment_id"] = str(resp.pop("comment_id"))
            author = db.users.find_one({"_id": resp["author"]})
            resp["author"] = {
                "name": author["name"],
                "photo": author["photo"]
            }
            if "likes" in resp:
                resp["liked"] = str(user_id) in resp["likes"]
            comm["responses"].insert(0, resp)
        author = db.users.find_one({"_id": comm["author"]})
        comm["author"] = {
            "name": author["name"],
            "photo": author["photo"]
        }
        comm.pop("practice_id")
        comm["id"] = str(comm.pop("_id"))
        if "likes" in comm:
            comm["liked"] = str(user_id) in comm["likes"]
        comments.append(comm)
        comments.reverse()
    return comments


def view_practice(practice_id, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    user = db.users.find_one({"email": payload["sub"]})
    try:
        practice = db.practices.find_one_and_update(
            {"_id": ObjectId(practice_id)}, {"$inc": {"views": 1}})
        practice.pop("_id")
        for author in practice["authors"]:
            if author["user_id"]:
                author_photo = db.users.find_one(
                    {"_id": author["user_id"]}, ["photo"])
                author_photo.pop("_id")
                author["user_id"] = str(author["user_id"])
                if "photo" in author_photo:
                    author["photo"] = author_photo["photo"]
        practice["comments"] = get_comments(practice_id, user_id=user["_id"])
        if "likes" in practice:
            practice["liked"] = str(user["_id"]) in practice["likes"]
        return practice
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


@router.get('/like')
def like_practice(practice_id: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    try:
        user = db.users.find_one({"email": payload["sub"]})
        pract = db.practices.find_one({"_id": ObjectId(practice_id)})
        likes = pract["likes"] if "likes" in pract else []
        if str(user["_id"]) in likes:
            db.practices.find_one_and_update(
                {"_id": ObjectId(practice_id)}, {"$pull": {"likes": str(user["_id"])}})
            return "deslike in practices"
        db.practices.find_one_and_update(
            {"_id": ObjectId(practice_id)}, {"$push": {"likes": str(user["_id"])}})
        # add_notification_like(pract, user)
        return "Like on practice"
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


def add_notification_like(pract, user):
    for author in pract["authors"]:
        if author["user_id"]:
            notification = {
                "user_id": author["user_id"],
                "type": "practice_like",
                "text": "User {username} liked your practice!".format(username=user["name"]),
                "practice_id": pract["_id"],
                "liker_id": user["_id"],
                "read": False,
                "date": datetime.now()
            }
            db.notifications.insert_one(notification)


@router.put('/')
def update_practice(practice_id: str,
                    practice: UpdatePractices,
                    token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    practice_data = {
        k: v
        for k,
        v in practice.dict().items() if v is not None
    }
    try:
        user = db.users.find_one({"email": payload["sub"]})
        db_practice = db.practices.find_one({"_id": ObjectId(practice_id)})
        if not user or not db_practice:
            raise HTTPException(
                status_code=401, detail="Author or practice not found")
        found = False
        for author in db_practice["authors"]:
            if author["user_id"] == user["_id"]:
                found = True
        if not found:
            raise HTTPException(
                status_code=401, detail="Author cannot modify practice")
        result = db.practices.update_one(
            {"_id": ObjectId(practice_id)}, {"$set": practice_data})
        return "practice updated {id}".format(id=practice_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=503, detail="Database error, try again later")
