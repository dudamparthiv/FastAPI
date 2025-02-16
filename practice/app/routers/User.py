from fastapi import APIRouter, Header,status,HTTPException,Depends,Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app import model
from app.controllers import User
from app import auth


router = APIRouter(
    prefix="/user",
    tags=["User"]
)

get_db = model.get_db


@router.post("/create_user/",status_code=status.HTTP_200_OK,response_model=model.user_id)
def create_user(form_data:model.user_public,db:Session =Depends(get_db)):
    return User.create_user(form_data,db)
    

@router.post("/login_user/",status_code=status.HTTP_200_OK)
def login_user(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    return User.login_user(form_data,db)


@router.get("/user_profile/",status_code=status.HTTP_200_OK,response_model = model.user_contact)
def profile(db:Session=Depends(get_db),current_user:model.user_id=Depends(auth.get_current_user)):
    return User.profile(db,current_user)
       

@router.delete("/delete_user/",status_code = status.HTTP_200_OK)
def delete_user(db:Session=Depends(get_db),current_user:model.user_id=Depends(auth.get_current_user)):
    return User.delete_user(db,current_user)
    

@router.get("/verify_token/")
def verify_user_token(token: str = Header(None)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        auth.verify_token(token=token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Token verification failed")

    return {"message": "Token is valid"}