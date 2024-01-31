import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, HTTPException
from hotels_example import example_obj
from dbConnections import basic_sql_queries
from prices_example import price_example_object
from fastapi.middleware.cors import CORSMiddleware
from moduls.beProApi import bepro_api
from moduls.algorithm import opportunity_response_handler

app = FastAPI()

search_opportunities_router = APIRouter()
bookings_router = APIRouter()
prices_router = APIRouter()


class SearchPostBody(BaseModel):
    search_key: str
    stars: int
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
async def search_opportunities(body: SearchPostBody):
    try:
        basic_sql_queries.insert_search_setting(body.stars, body.search_key)
        return {"massage": "The request was successfully received - search setting added successfully"}
    except HTTPException:
        return HTTPException(status_code=500)


@bookings_router.get('/')
async def charge_condition(room_token, price):
    try:
        info_grass_rate = bepro_api.check_charge_condition(room_token, price)
        if info_grass_rate[0]:
            return {"massage": f"Warning the price has changed! The current price - {info_grass_rate[1]} "
                               f"The previous price - {price}"}
        return {"massage": f"The price has not changed {price}"}
    except HTTPException:
        return HTTPException(status_code=500)


@search_opportunities_router.get('/')
async def get_opportunities():
    try:
        return opportunity_response_handler.get_opportunities_response()
    except HTTPException:
        return HTTPException(status_code=500)


@prices_router.get('/')
async def get_prices(hotel_id, room_id):
    try:
        return price_example_object
    except HTTPException:
        return HTTPException(status_code=500)


app.include_router(search_opportunities_router, prefix='/api/search_opportunities')
app.include_router(search_opportunities_router, prefix='/api/search_opportunities/opportunities')
app.include_router(prices_router, prefix='/api/search_opportunities/prices')
app.include_router(bookings_router, prefix='/api/search_opportunities/bookings')

uvicorn.run(app, host='127.0.0.1', port=8000, access_log=False)
