from sqlalchemy import Column, Integer, String
from database import Base
class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {'extend_existing': True}  

    id = Column(Integer, primary_key=True, index=False)
    title = Column(String, index=True)
    body = Column(String, index=True)