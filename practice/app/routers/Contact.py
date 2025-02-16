from fastapi import APIRouter,status,Depends
from sqlmodel import Session
from app import auth, model
from app.controllers import Contact

router = APIRouter(
    prefix="/contact",
    tags=["Contacts"]
)

get_db = model.get_db


@router.post("/create_contact/",status_code=status.HTTP_200_OK,response_model=model.contact_user)
def create_contact(request:model.contact,db:Session =Depends(get_db),current_user:model.user_id=Depends(auth.get_current_user)):
    return Contact.create_contact(request,db,current_user)


@router.put("/update_contact/{id}",status_code=status.HTTP_200_OK,response_model=model.contact_user)
def update_contact(id:int,request:model.contact,db:Session =Depends(get_db),current_user:model.user_id=Depends(auth.get_current_user)):
    return Contact.update_contact(id,request,db)


@router.delete("/delete_contact/{id}",status_code=status.HTTP_200_OK)
def delete_contact(id:int,db:Session =Depends(get_db),current_user:model.user_id=Depends(auth.get_current_user)):
    return Contact.delete_contact(id,db)


@router.delete("/delete_all_contacts/",status_code=status.HTTP_200_OK)
def delete_all_contact(db:Session =Depends(get_db),current_user:model.user_id=Depends(auth.get_current_user)): 
    return Contact.delete_all_contact(db,current_user)
