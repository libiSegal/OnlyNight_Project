import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, HTTPException
from moduls.beProApi import bepro_api
from example import example_obj

app = FastAPI()

search_opportunities_router = APIRouter()


class PostBody(BaseModel):
    search_key: str
    stars: int
    check_in: str
    check_out: str
    num_adults: int
    num_children: int
    children_age: list


@search_opportunities_router.post('/')
async def search_opportunities(body: PostBody):
    geo_code = {
        "Latitude": "52.52000659999999",
        "Longitude": "13.404954",
        "PIP": "N"
    }
    try:
        bepro_api.search_hotels(body.search_key, geo_code, body.stars, body.check_in, body.check_out, body.num_adults,
                                body.num_children, body.children_age)
        return "The request was successfully received"
    except HTTPException as e:
        return HTTPException(status_code=500)


@search_opportunities_router.get('/')
async def get_opportunities():
    return example_obj


app.include_router(search_opportunities_router, prefix='/api/search_opportunities')
app.include_router(search_opportunities_router, prefix='/api/search_opportunities/opportunities')

uvicorn.run(app, host='127.0.0.1', port=8000)
