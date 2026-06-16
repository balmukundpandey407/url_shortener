from sqlalchemy import Column,String
from sqlalchemy.orm import relationship
from app.database.url import Base

class User(Base):
    __tablename__="Users"

    id= Column(String,primary_key=True)
    name=  Column(String)
    email=  Column(String)
    hashed_password=  Column(String)
    created_at=  Column(String)
    
    Urls = relationship("URL", back_populates="owner")
