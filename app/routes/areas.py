from fastapi import Depends, APIRouter, HTTPException
from app.controllers.security import decode_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.db.connection import db
from app.models.enums import SWEBOK

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(
    prefix="/areas",
    responses={404: {"description": "Not found"}},
)


@router.get("/likes")
def get_likes_areas(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    likes = [{"label": e.value, "value": 0} for e in SWEBOK]
    for pract in db.practices.find():
        count = len(pract["likes"]) if "likes" in pract else 0
        for area in pract["swebok"]:
            for like in likes:
                if like["label"] == area:
                    like["value"] = like["value"] + count
    return likes



@router.get("/views")
def get_views_areas(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    views = [{"label": e.value, "value": 0} for e in SWEBOK]
    for pract in db.practices.find():
        count = pract["views"] if "views" in pract else 0
        for area in pract["swebok"]:
            for view in views:
                if view["label"] == area:
                    view["value"] = view["value"] + count
    return views


@router.get("/comments")
def get_comments_areas(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    comments = [{"label": e.value, "value": 0} for e in SWEBOK]
    for pract in db.practices.find():
        count = db.comments.find({"practice_id": pract["_id"]}).count()
        for area in pract["swebok"]:
            for comm in comments:
                if comm["label"] == area:
                    comm["value"] = comm["value"] + count
    return comments
