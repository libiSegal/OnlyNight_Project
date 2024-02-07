class HotelData:
    search_id: int
    hotel_name: str
    hotel_code: str
    hotel_stars: float
    hotel_address: str
    hotel_phone: str | None
    hotel_fax: str | None
    hotel_city: str
    hotel_country: str
    hotel_latitude: str
    hotel_longitude: str
    hotel_pip: str

    def __init__(self, search_id, name, code, stars, address, phone, fax, city, country, latitude, longitude, pip):
        self.search_id = search_id
        self.hotel_name = name
        self.hotel_code = code
        self.hotel_stars = stars
        self.hotel_address = address
        self.hotel_phone = phone
        self.hotel_fax = fax
        self.hotel_city = city
        self.hotel_country = country
        self.hotel_latitude = latitude
        self.hotel_longitude = longitude
        self.hotel_pip = pip

