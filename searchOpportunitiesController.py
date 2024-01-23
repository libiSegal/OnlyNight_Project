import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, HTTPException
from hotels_example import example_obj
from moduls.beProApi import bepro_api
from prices_example import price_example_object
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

search_opportunities_router = APIRouter()
prices_router = APIRouter()


class PostBody(BaseModel):
    search_key: str
    stars: int
    check_in: str
    check_out: str
    num_adults: int
    num_children: int
    children_age: list


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    print("Search opportunities")
    return example_obj


@prices_router.get('/')
async def get_prices(hotel_id, room_id):
    print("Getting prices")
    return price_example_object


app.include_router(search_opportunities_router, prefix='/api/search_opportunities')
app.include_router(search_opportunities_router, prefix='/api/search_opportunities/opportunities')
app.include_router(prices_router, prefix='/api/search_opportunities/prices')

uvicorn.run(app, host='127.0.0.1', port=8000, access_log=False)
