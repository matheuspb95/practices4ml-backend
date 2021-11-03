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
        for author in practice.authors:
            if (author.user_id and not db.users.find_one({"_id": ObjectId(author.user_id)})):
                raise HTTPException(
                    status_code=401, detail="Author id not existent")
        practice.create_date = datetime.now()
        result = db.practices.insert_one(practice.dict())
        return "practice created {id}".format(id=result.inserted_id)
    except:
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


@router.get("/")
def get_practices(
        practice_id: str = None,
        search: str = '',
        skip: int = 0,
        limit: int = 0,
        token: str = Depends(oauth2_scheme)):
    if practice_id:
        return view_practice(practice_id)
    payload = decode_token(token)
    practices = []
    regex = re.compile("^{search}".format(search=search), flags=re.IGNORECASE)
    try:
        user = db.users.find_one({"email": payload["sub"]})
        for prat in db.practices.find({"name": {"$regex": regex}}).skip(skip).limit(limit):
            editable = False
            prat["id"] = str(prat.pop("_id"))
            for author in prat["authors"]:
                if author["user_id"]:
                    if author["user_id"] == user["_id"]:
                        editable = True
                    author_photo = db.users.find_one(
                        {"_id": author["user_id"]}, ["photo"])
                    author_photo.pop("_id")
                    author["user_id"] = str(author["user_id"])
                    if "photo" in author_photo:
                        author["photo"] = author_photo["photo"]
            prat["editable"] = editable
            practices.append(prat)
        return practices
    except:
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


def view_practice(practice_id):
    practice = db.practices.find_one({"_id": ObjectId(practice_id)})
    practice.pop('_id')
    practice["likes"] = 5
    practice["views"] = 50
    practice["comments"] = [
        {
            "author": {
                "name": "MATHEUS PALHETA",
                "photo": ""
            },
            "comment": "nice practice bro",
            "likes": 1,
            "date": datetime.now(),
            "responses": [
                {
                    "author": {
                        "name": "Eliza",
                        "photo": ""
                    },
                    "comment": "I like it too",
                    "likes": 1,
                    "date": datetime.now(),
                }
            ]
        }
    ]
    return practice


@router.put('/')
def update_practices(practice_id: str,
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
    except:
        raise HTTPException(
            status_code=503, detail="Database error, try again later")
