from fastapi import HTTPException,status
from blogs import model



def get_all_blogs(db):
    blogs = db.query(model.Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NotFound")
    return blogs

def create_blog(form_data,db):
    blog = model.Blog(name= form_data.name, description=form_data.description)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def update_blog(id,name,description,db):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NotFound")
    blog.name = name
    blog.description = description
    db.commit()
    return "Updated Successfully"

def delete_blog(id,db):
    blog = db.query(model.Blog).filter(model.Blog.id == id).delete()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NotFound")
    db.commit()
    return "deleted Successfully"

def delete_all_blog(db):
    blogs = db.query(model.Blog).delete()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NotFound")
    db.commit()
    return "deleted Successfully"