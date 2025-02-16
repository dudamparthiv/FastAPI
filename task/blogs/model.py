from sqlmodel import SQLModel,Field,create_engine,Session

class blog(SQLModel):
    name:str
    description:str

class Blog(blog,table=True):
    id: int | None = Field(default=None,primary_key=True,index=True)
    
engine = create_engine("sqlite:///./blogs/database.db",connect_args={"check_same_thread":False})
SQLModel.metadata.create_all(engine)
def get_db():
    with Session(engine) as session:
        yield session
