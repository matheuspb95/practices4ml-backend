from fastapi import APIRouter, HTTPException
from app.db.connection import db
from app.models.models import CreateUserModel, LoginModel, UpdateUserModel
from app.controllers.validations import check_obj
from app.controllers.security import get_password_hash


router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_user(user: CreateUserModel):
    check_obj(user)
    if(db.users.find_one({"email":user.email})):
        raise HTTPException(
            status_code=409, detail="{email} already in use".format(email=user.email))
    db_user = user.dict()
    db_user['password'] = get_password_hash(db_user.pop('password'))
    result = db.users.insert(db_user)
    if result.writeConcernError or result.writeError:
        raise HTTPException(
            status_code=503, detail="Database error, try again later")
    return "user {email} created".format(email=db_user["email"])


@router.post("/login")
def create_user(user: LoginModel):
    # Validar email e senha
    # Verificar email no banco
    # verificar senha cifrada
    # returnar token
    return "login"

@router.put("/")
def update_user(user: UpdateUserModel):
    # validar nome, email, work, degree, areas
    db.users.update_one(user.dict())
    # retornar OK/NOTOK
