from fastapi import APIRouter, Form,status,Depends,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from blogs import model
from blogs.controllers import Blog

router = APIRouter(
    tags=["Blogs"]
)

templates = Jinja2Templates(directory="blogs/templates")

get_db = model.get_db


@router.get("/", response_class=HTMLResponse)
def read_blogs(request: Request, db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs})

@router.get("/",status_code=status.HTTP_200_OK,response_model=list[model.Blog])
def get_all_blogs(db:Session= Depends(get_db)):
    Blogs= Blog.get_all_blogs(db)
    return Blogs


@router.get("/create_blog/", response_class=HTMLResponse)
def create_blog(request: Request, db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return templates.TemplateResponse("create_blog.html", {"request": request, "blogs": blogs})

@router.post("/create_blog/",status_code=status.HTTP_200_OK,response_model=model.Blog)
def create_blog(form_data:model.blog =Form(...),db:Session= Depends(get_db)):
    return Blog.create_blog(form_data,db)


@router.get("/update_blog/{id}", response_class=HTMLResponse)
def update_blog(id:int,request: Request, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    return templates.TemplateResponse("update_blog.html", {"request": request, "blog": blog})

@router.put("/update_blog/{id}",status_code=status.HTTP_200_OK)
def update_blog(id:int,name:str =Form(...),description:str = Form(...),db:Session= Depends(get_db)):
    return Blog.update_blog(id,name,description,db)
    

@router.get("/delete_blog/{id}", response_class=HTMLResponse)
def delete_blog(id:int,request: Request, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    return templates.TemplateResponse("delete_blog.html", {"request": request, "blog": blog})

@router.delete("/delete_blog/{id}",status_code=status.HTTP_200_OK)
def delete_blog(id:int,db:Session= Depends(get_db)):
    return Blog.delete_blog(id,db)


@router.get("/delete_all_blogs/", response_class=HTMLResponse)
def delete_blog(request: Request, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).all()
    return templates.TemplateResponse("delete_all_blogs.html", {"request": request, "blog": blog})

@router.delete("/delete_all_blogs/",status_code=status.HTTP_200_OK)
def delete_all_blog(db:Session= Depends(get_db)):
    return Blog.delete_all_blog(db)