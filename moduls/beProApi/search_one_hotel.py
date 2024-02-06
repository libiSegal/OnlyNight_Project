from datetime import datetime
from moduls.beProApi import bepro_api
from dbConnections import sql_queries
from moduls.algorithm import statisticall_information
from moduls.objects.response_opportunity_obj import ResponseOpportunityItem, ResponseOpportunityImg, \
    ResponseOpportunityHotel, ResponseOpportunity


def search_one_hotel(hotel_name, stars, check_in, check_out, radius):
    check_in = datetime.strptime(check_in, "%Y-%m-%d")
    check_out = datetime.strptime(check_out, "%Y-%m-%d")
    return bepro_api.search_hotels("hotel", hotel_name, stars, check_in, check_out, radius)


def get_rooms_prices_from_db(ids):
    return sql_queries.select_room_price_by_id(ids)


def calculate_opportunities(room_prices, segment, last_year, arbitrage=50):
    opportunities = []
    month = get_the_check_in_month(room_prices[0])
    history_data = statisticall_information.get_statistically_information_for_segment(segment, month, last_year)
    if len(history_data) != 0:
        history_price = statisticall_information.get_adr_for_month(history_data)
        for room in room_prices:
            if room[1] + arbitrage <= history_price:
                opportunities.append(room[0])
    return opportunities


def get_the_check_in_month(room):
    return datetime.strptime(room[2], "%Y-%m-%d %H:%M:%S").month


def get_rooms_data_from_db(ids):
    return sql_queries.select_data_of_opportunities(ids)


def select_hotel_data(room):
    hotel_id = room[1]
    return sql_queries.select_data_of_hotels_by_id(hotel_id)


def fill_hotel_data(data_hotel):
    images = []
    for data in data_hotel:
        images.append(ResponseOpportunityImg(data[-1], data[-2]).body)
    item = ResponseOpportunityItem()
    item.validate_data(*data_hotel[0][:-2])
    item.add_images(images)
    return item.body


def fill_room_data(data_rooms):
    rooms = []
    for data in data_rooms:
        data.pop(1)
        rooms.append(create_room(*data))
    return rooms


def create_room(room_id, price, desc, sys_code, check_in, check_out, nights, token,
                limit_date, remarks, meal_plan_code, meal_plan_desc):
    body = {"RoomId": room_id, "Desc": desc, "Price": price, "SysCode": sys_code, "NumAdt": 2, "NumCnn": 0,
            "CnnAge": [], "CheckIn": check_in, "CheckOut": check_out, "Nights": nights, "BToken": token,
            "LimitDate": limit_date, "Remarks": remarks, "MetaData": {}}
    body["MetaData"]["Code"] = meal_plan_code
    body["MetaData"]["Desc"] = meal_plan_desc
    return body


def fill_response_data(item, rooms):
    hotel = ResponseOpportunityHotel(item, rooms)
    return ResponseOpportunity([hotel.body]).body


def extract_data_from_sql_type(data):
    room_data = []
    for item in data:
        room_data.append(list(item))
    return room_data


def get_last_year():
    return datetime.now().year - 1


def check_if_segment(city):
    search_settings = sql_queries.select_search_setting()
    for search_setting in search_settings:
        if city in search_setting[0]:
            return True
        else:
            return False


def check_correctness_of_the_hotel_name(hotel_name, hotel_name_to_check):
    print(hotel_name, hotel_name_to_check)
    return hotel_name == hotel_name_to_check


def bePro_search_one(hotel_name, stars, check_in, check_out, segment, radius, arbitrage):
    if not check_if_segment(segment):
        return Exception("This city is not under surveillance")
    if hotel_name == "":
        rooms_ids = search_one_hotel(segment, stars, check_in, check_out, radius)
    else:
        rooms_ids = search_one_hotel(hotel_name, stars, check_in, check_out, radius=1)
    if rooms_ids:
        rooms_ids = list(set(rooms_ids))
        prices = get_rooms_prices_from_db(rooms_ids)
        last_year = get_last_year()
        oppo = calculate_opportunities(prices, segment, last_year, arbitrage)
        if len(oppo) > 0:
            oppo_data = get_rooms_data_from_db(oppo)
            hotel_data = select_hotel_data(oppo_data[0])
            oppo_data = extract_data_from_sql_type(oppo_data)
            item = fill_hotel_data(hotel_data)
            if check_correctness_of_the_hotel_name(item.get("Name"), hotel_data[0][1]):
                rooms = fill_room_data(oppo_data)
                hotel = ResponseOpportunityHotel(item, rooms)
                return hotel.body
            else:
                "No opportunities exist for this hotel"
        else:
            return "No opportunities exist for these values"
    else:
        return "No information exists for these values"
