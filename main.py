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

#uvicorn main:app --host 0.0.0.0 --port 80 --reload
#nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload >> __public_logs__/out 2>> __public_logs__/error &
#nohup python -u app.py >> __public_logs__/out 2 >> __public_logs__/error &
#sudo kill -9 `sudo lsof -t -i:8000`
    