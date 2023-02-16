from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import hsn_scrapper

class params(BaseModel):
    HSN: str
    
app = FastAPI()

@app.get("/")
async def home():
    return {"message": "server is on"}

@app.post("/data/")
async def get_data(data: params):
    data = data.dict()
    d = {}
    d['hsn_descp'],d['hsn_data'] = hsn_scrapper.dgcis_scrapper(data['HSN'])
    return d
    