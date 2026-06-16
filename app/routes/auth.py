from fastapi import FastAPI, APIRouter, Depends,HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import session

import uuid
import datetime

from app.database.url import get_db,engine
from app.database.url import Base
from app.models.user import User
from app.models.urls import URL
from app.core.services.auth import security,hashpassword, verifypassword, sign_jwt, decode_jwt
from app.schemas.user import Create_User, Login_User,Out_User


auth_route = APIRouter()

Base.metadata.create_all(bind=engine)

def get_current_user(
    db: session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials
    decoded_token = decode_jwt(token)

    if not decoded_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.id == decoded_token["user_id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return Out_User(
        id = user.id,
        name = user.name,
        email = user.email
    )


@auth_route.post("/register")
def sign_up_user(sign_up_data: Create_User, db: session = Depends(get_db)):

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == sign_up_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists please login instead")

    # Hash the password
    hashed_password = hashpassword(sign_up_data.password)
    
    new_user = User(
     id= str(uuid.uuid4()),
     name = sign_up_data.name,
     email = sign_up_data.email,
     hashed_password = hashed_password,
     created_at = datetime.datetime.now()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@auth_route.post("/login")
def Login_User(login_data: Login_User,db: session=Depends(get_db)):

    #check user by email
    user=db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verifypassword(login_data.password,user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = sign_jwt(user.id)

    return token

