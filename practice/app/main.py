from fastapi import FastAPI
from app.routers import Contact, User

app = FastAPI()


app.include_router(User.router)
app.include_router(Contact.router)
