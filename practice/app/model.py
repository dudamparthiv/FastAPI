from pydantic import EmailStr,BaseModel
from sqlmodel import SQLModel,create_engine,Field,Relationship,Session

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class user(SQLModel):
    name:str
    email:EmailStr

class user_id(user):
    id:int
class user_contact(user_id):
    contacts: list["contact_id"]
class user_public(user):
    password:str

class User(user_public,table=True):
    id : int | None = Field(default=None,primary_key=True,index=True)
    contacts: list["Contact"] = Relationship(back_populates="creator")


class contact(SQLModel):
    name:str
    phone:str

class contact_id(contact):
    id:int

class contact_user(contact_id):
    creator:user_id

class Contact(contact,table=True):
    id : int | None = Field(default=None,primary_key=True,index=True)
    user_id : int | None =Field(foreign_key="user.id")
    creator : User = Relationship(back_populates="contacts")

DATABASE_URL = "sqlite:///./app/contact.db"
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
