from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.db.connection import db
from app.models.models import CreateUserModel, Token, UpdateUserModel
from app.controllers.validations import check_obj
from app.controllers.security import get_password_hash, authenticate_user, decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

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
    try:
        db.users.insert_one(db_user)
        return "user {email} created".format(email=db_user["email"])
    except:
        raise HTTPException(
            status_code=503, detail="Database error, try again later")


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = authenticate_user(db, form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}
    

@router.put("/")
def update_user(user: UpdateUserModel, token: str = Depends(oauth2_scheme)):
    check_obj(user)
    payload = decode_token(token)
    if (not payload['sub'] == user.email):
        raise HTTPException(
            status_code=401, detail="User not authenticated")
    result = db.users.update_one({"email": user.email}, { "$set": user.dict()})
    if (not result.modified_count):
        raise HTTPException(
            status_code=400, detail="No user found or modified")
    return "User {} saved".format(user.email)
