from pydantic import BaseModel

class Create_Short_URL(BaseModel):
    url: str
    code: str

class Update_OG_URL(BaseModel):
    id:str
    url:str
