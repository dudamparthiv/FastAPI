from fastapi import status,HTTPException
from app import model,auth 
from app.routers import Contact


def create_user(form_data,db):
    user = db.query(model.User).filter((model.User.name == form_data.name) | (model.User.email == form_data.email)).first()
    if user:
        raise HTTPException(status_code=status.HTTP_302_FOUND,detail="User Already Exists")
    hashed_password = auth.hashed(form_data.password)
    create_user = model.User(
          name = form_data.name,
          email = form_data.email,
          password= hashed_password
          )
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return user


def login_user(form_data,db):
    login = db.query(model.User).filter((model.User.email == form_data.username) | (model.User.name == form_data.username)).first()
    if not login:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Creadentials")
    if not auth.verify(form_data.password,login.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Password")
    access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": login.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"} 


def profile(db,current_user):
    user = db.query(model.User).filter(model.User.id == current_user.id ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,deatil="Not Found")
    return user


def delete_user(db,current_user):
    delete = db.query(model.User).filter(model.User.id == current_user.id).first()
    if not delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Not Found")
    Contact.delete_all_contact(db,current_user)
    db.delete(delete)
    db.commit()
    return "Deleted Successfully"

