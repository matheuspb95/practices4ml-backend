from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from bson.objectid import ObjectId
from app.db.connection import db
from app.models.models import CreatePractices
from app.controllers.validations import check_obj

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
        result = db.practices.insert_one(practice.dict())
        return "practice created {id}".format(id=result.inserted_id)
    except:
        raise HTTPException(
            status_code=503, detail="Database error, try again later")
