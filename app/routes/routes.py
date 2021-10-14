from fastapi import APIRouter
from app.db.connection import db
from app.models.models import UserModel

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


@router.post("/new")
def create_user(user: UserModel):
    db.users.insert(user.dict())


@router.get("/")
def read_users():
    users = []
    for user in db.users.find():
        users.append(UserModel(**user))
    return users

