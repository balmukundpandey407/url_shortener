from pydantic import BaseModel,EmailStr
from typing import Optional

class Create_User(BaseModel):
    name : str
    email : EmailStr
    password : str

class Login_User(BaseModel):
    email: EmailStr
    password: str 

class Out_User(BaseModel):
    id:str
    name: str
    email: EmailStr