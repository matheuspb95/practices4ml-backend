from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from bson.objectid import ObjectId
from app.db.connection import db
from app.models.models import CreateComment
from app.controllers.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/comments",
    responses={404: {"description": "Not found"}},
)


@router.post('/')
def add_comment(comment: CreateComment, comment_id: str = None, practice_id: str = None, token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user = db.users.find_one({"email": payload["sub"]})
        if not user:
            raise HTTPException(
                status_code=401, detail="User not found")

        if comment_id:
            comm = db.comments.find_one({"_id": ObjectId(comment_id)})
            if not comment:
                raise HTTPException(
                    status_code=401, detail="Practice not found")

            resp = {
                "comment": comment.comment,
                "author": user["_id"],
                "date": datetime.now(),
                "comment_id": comm["_id"],
                "likes": [],
            }
            result = db.comments.insert_one(resp)
            if not result:
                raise HTTPException(
                    status_code=401, detail="Practice not found")
            return "Response added"

        practice = db.practices.find_one({"_id": ObjectId(practice_id)})
        if not practice:
            raise HTTPException(
                status_code=401, detail="Practice not found")

        comm = {
            "comment": comment.comment,
            "author": user["_id"],
            "date": datetime.now(),
            "practice_id": practice["_id"],
            "likes": [],
        }
        result = db.comments.insert_one(comm)

        if not result:
            raise HTTPException(
                status_code=401, detail="Practice not found")
        return "Comment added"
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


@router.get('/like')
def like_comment(comment_id: str, token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    try:
        user = db.users.find_one({"email": payload["sub"]})
        likes = db.comments.find_one({"_id": ObjectId(comment_id)})["likes"]
        if str(user["_id"]) in likes:
            db.comments.find_one_and_update(
                {"_id": ObjectId(comment_id)}, {"$pull": {"likes": str(user["_id"])}})
            return "deslike in comment"
        db.comments.find_one_and_update(
            {"_id": ObjectId(comment_id)}, {"$push": {"likes": str(user["_id"])}})
        return "Like on comment"

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=503, detail="Database error, try again later")
