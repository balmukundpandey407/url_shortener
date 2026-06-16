from fastapi import APIRouter, Depends,HTTPException
from fastapi.responses import RedirectResponse

from app.database.url import get_db,engine
from sqlalchemy.orm import session
from app.database.url import Base
from app.models.user import User
from app.models.urls import URL
from app.routes.auth import get_current_user

import uuid
import shortuuid
from datetime import datetime,timedelta

url_route = APIRouter()

Base.metadata.create_all(bind=engine)

@url_route.post("/short_url")
def Create_Short_URL(OG_url:str,db: session=Depends(get_db),current_user= Depends(get_current_user)):

    if db.query(URL).filter(URL.original_url == OG_url,URL.user_id == current_user.id).first():
        raise HTTPException(status_code=400,detail="URL already exists")
    
    code= shortuuid.ShortUUID().random(length=8)

    data=URL(
     id= str(uuid.uuid4()),
     original_url= OG_url,
     short_code= code,
     user_id= current_user.id,
     click_count= 0,
     expires_at= datetime.now()+timedelta(days=90),
     created_at= datetime.now()
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return data

@url_route.get("/short_url/{code}")
def redirect(code:str,db: session=Depends(get_db)):

    url=db.query(URL).filter(URL.short_code == code).first()

    if not url:
        raise HTTPException(status_code=404,detail="URL not found")

    if url.expires_at < datetime.now():
       raise HTTPException(status_code = 410, detail= "url has expired")

    url.click_count +=1
    
    db.commit()

    return RedirectResponse(url=url.original_url,status_code=302)

   

@url_route.post("/short_url/{custom_code}")
def custom_alias(custom_code:str,OG_url: str ,db: session=Depends(get_db),current_user= Depends(get_current_user)):

    if db.query(URL).filter(URL.original_url == OG_url,URL.user_id == current_user.id).first():
        raise HTTPException(status_code=400,detail="URL already exists")

    if db.query(URL).filter(URL.short_code == custom_code).first():
        raise HTTPException(status_code=400,detail="code already exists")

    data=URL(
     id= str(uuid.uuid4()),
     original_url= OG_url,
     short_code= custom_code,
     user_id= current_user.id,
     click_count= 0,
     expires_at= datetime.now()+timedelta(days=90),
     created_at= datetime.now()
    )

    db.add(data)
    db.commit()
    db.refresh(data)

    return data

@url_route.get("/short_url/exp/{code}")
def check_expiry( code:str,db: session=Depends(get_db),current_user= Depends(get_current_user)):
    
    url=db.query(URL).filter(URL.short_code == code).first()
    
    return{"short url will expires at": url.expires_at}

