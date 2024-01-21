import pydantic


class HotelData(pydantic.BaseModel):
    hotel_name: str
    hotel_code: str
    hotel_stars: float
    hotel_address: str
    hotel_phone: str
    hotel_fax: str
    hotel_Latitude: str
    hotel_Longitude: str
    hotel_pip: str
    hotel_city: str
    hotel_country: str
