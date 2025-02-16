from fastapi import status,HTTPException
from app import model


def create_contact(request,db,current_user):
    contact = model.Contact(
        name= request.name,
        phone= request.phone,
        user_id = current_user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_contact(id,db):
    contact = db.query(model.Contact).filter(model.Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    return contact


def update_contact(id,request,db):
    
    contact = db.query(model.Contact).filter(model.Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    contact.name= request.name
    contact.phone = request.phone
    db.commit()
    return contact


def delete_contact(id,db):
    contact = db.query(model.Contact).filter(model.Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    db.delete(contact)
    db.commit()
    return "Deleted Successfull"


def delete_all_contact(db,current_user):
    contact = db.query(model.Contact).filter(model.Contact.user_id == current_user.id).delete()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    db.commit()
    return "Deleted Successfull"