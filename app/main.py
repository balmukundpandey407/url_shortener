from fastapi import FastAPI
from app.routes.url import url_route
from app.routes.auth import auth_route

app = FastAPI()

@app.get('/')
def home():
    return {"message":"URL_shortner Working Properly"}

app.include_router(url_route)
app.include_router(auth_route)