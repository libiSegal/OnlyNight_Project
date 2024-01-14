import datetime
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, Form

app = FastAPI()

search_opportunities_router = APIRouter()


class Body(BaseModel):
    search_key: str
    starts: int
    check_in: str
    check_out: str


@search_opportunities_router.post('/')
async def search_opportunities(body: Body):
    print("Search Opportunities")
    return 'Search Opportunities'


app.include_router(search_opportunities_router, prefix='/search_opportunities')

uvicorn.run(app, host='127.0.0.2', port=8080)
