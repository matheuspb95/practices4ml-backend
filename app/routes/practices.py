from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from bson.objectid import ObjectId
from app.db.connection import db
from app.models.models import CreatePractices
from app.controllers.validations import check_obj
from typing import List
import re

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/practices",
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_practice(practice: CreatePractices):
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
def list_practices(search: str = '', skip: int = 0, limit: int = 0):
    practices = []
    regex = re.compile("^{search}".format(search=search), flags=re.IGNORECASE)
    for prat in db.practices.find({"name": {"$regex": regex}}).skip(skip).limit(limit):
        prat["id"] = str(prat.pop("_id"))
        for author in prat["authors"]:
            if author["user_id"]:
                author["user_id"] = str(author["user_id"])
        practices.append(prat)
    return practices
