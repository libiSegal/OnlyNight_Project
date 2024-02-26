import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, HTTPException
from dbConnections import sql_queries
from fastapi.middleware.cors import CORSMiddleware
from moduls.beProApi import bepro_api
from moduls.algorithm import opportunity_response_handler
from moduls.algorithm import calculate_hotel_price
from moduls.beProApi import search_one_hotel

app = FastAPI()

search_opportunities_router = APIRouter()
search_one_hotel_opportunities_router = APIRouter()
hotels_names_router = APIRouter()
bookings_router = APIRouter()
prices_router = APIRouter()


class SearchHotelsPostBody(BaseModel):
    search_key: str
    stars: int
    num_adults: int
    num_children: int
    children_age: list


class SearchOneHotelPostBody(BaseModel):
    city: str
    hotel_name: str
    stars: float
    check_in: str
    check_out: str
    price: float
    location: float


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@search_opportunities_router.post('/')
async def search_opportunities(body: SearchHotelsPostBody):
    try:
        sql_queries.insert_search_setting(body.stars, body.search_key)
        return {"massage": "The request was successfully received - search setting added successfully"}
    except HTTPException:
        return HTTPException(status_code=500)


@search_one_hotel_opportunities_router.post('/')
async def search_one_hotels(body: SearchOneHotelPostBody):
    try:
        return search_one_hotel.bePro_search_one(body.hotel_name, body.stars, body.check_in, body.check_out, body.city,
                                                 body.location, body.price)
    except HTTPException:
        return HTTPException(status_code=500, detail="Sorry, an error occurred")


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
        hotels = opportunity_response_handler.get_opportunities_response()
        for hotel in hotels.get("Hotels"):
            print(hotel.get("Item").get("Name"), len(hotel.get("Rooms")))
            for room in hotel.get("Rooms"):
                print(room.get("Desc"))
        return hotels
    except HTTPException:
        return HTTPException(status_code=500, detail="Sorry, an error occurred")


@prices_router.get('/{hotel_id}')
async def get_prices(hotel_id: str):
    try:
        return calculate_hotel_price.get_hotel_room_classes(hotel_id)
    except HTTPException:
        return HTTPException(status_code=500)


@hotels_names_router.get('/')
async def get_hotels_names():
    hotels = sql_queries.select_hotels_name()
    hotels_set = set(hotels)
    return {"Hotels": hotels_set}


app.include_router(search_opportunities_router, prefix='/api/search_opportunities')
app.include_router(search_opportunities_router, prefix='/api/search_opportunities/opportunities')
app.include_router(search_one_hotel_opportunities_router, prefix='/api/search_opportunities/one_hotel')
app.include_router(prices_router, prefix='/api/search_opportunities/prices')
app.include_router(bookings_router, prefix='/api/search_opportunities/bookings')
app.include_router(hotels_names_router, prefix='/api/search_opportunities/hotels_names')

uvicorn.run(app, host='127.0.0.1', port=8000, access_log=False)
