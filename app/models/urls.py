from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from app.database.url import Base
from sqlalchemy.orm import relationship

class URL(Base):
    __tablename__="Urls"
    id= Column(String,primary_key=True)
    original_url= Column(String)
    short_code= Column(String)
    user_id= Column(String,ForeignKey("Users.id"))
    click_count= Column(Integer)
    expires_at= Column(DateTime)
    created_at= Column(DateTime)

    owner = relationship("User", back_populates="Urls")

