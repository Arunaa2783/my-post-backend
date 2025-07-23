from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    body: str

class PostCreate(PostBase):
    pass

class PostSchema(PostBase):
    id: int

    class Config:
        orm_mode = True
