from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {"message":"URL_shortner Working Properly"}

