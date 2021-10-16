from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.db.connection import db
from app.models.models import CreateUserModel, Token, UpdateUserModel
from app.controllers.validations import check_obj
from app.controllers.security import get_password_hash, authenticate_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
    result = db.users.insert_one(db_user)
    if result.writeConcernError or result.writeError:
        raise HTTPException(
            status_code=503, detail="Database error, try again later")
    return "user {email} created".format(email=db_user["email"])


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = authenticate_user(db, form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}
    

@router.put("/")
def update_user(user: UpdateUserModel, token: str = Depends(oauth2_scheme)):
    # validar nome, email, work, degree, areas
    db.users.update_one(user.dict())
    # retornar OK/NOTOK
