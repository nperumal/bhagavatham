from fastapi import FastAPI, Depends
from pydantic import BaseModel
from service.bhagavathamsearch import BhagavathamSearchService
from config import *

app = FastAPI()
service = None

class Query(BaseModel):
    text: str

async def get_service():
    global service 
    if service is None:
        service = BhagavathamSearchService(SENTENCE_TRANSFORMER_MODEL, MEANING_INDEX_NAME)
    return service

@app.on_event("startup")
async def startup_event():
    global service
    service = await get_service()

@app.post("/search")
async def search(query: Query, service: BhagavathamSearchService = Depends(get_service)):
    results = service.search(query.text)
    return results

@app.get("/poems")
async def poems(service: BhagavathamSearchService = Depends(get_service)):
    results = service.get_poems()
    return results