import pydantic

class HotelData(pydantic.BaseModel):
    hotel_name: str
    hotel_address: str
    hotel_price:float
