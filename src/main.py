from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Union
from src.test import main  # se lanci da fuori src

app = FastAPI() 

class ProcessRequest(BaseModel):
    url: HttpUrl
    cp: Union[int, float]

@app.post("/process")
async def process(request: ProcessRequest):
    # Puoi usare request.url e request.cp qui
    trace_url = await (main(request.url, request.cp))
    return {
        "message": "Elaborazione completata",
        "received_url": request.url,
        "received_cp": request.cp,
        "trace_url": trace_url
    }   