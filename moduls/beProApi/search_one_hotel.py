from datetime import datetime
from moduls.beProApi import bepro_api
from dbConnections import sql_queries
from moduls.algorithm import statisticall_information
from moduls.algorithm import opportunity_response_handler
from moduls.objects.response_opportunity_obj import ResponseOpportunityItem, ResponseOpportunityImg, \
    ResponseOpportunityHotel, ResponseOpportunity


def search_one_hotel(search_id, hotel_name, stars, check_in, check_out, radius):
    """
    Call the bePro_api to search the hotel
    :param search_id: the id of the city of the hotel
    :param hotel_name: the name of the hotel to search
    :param stars: the number of stars of hotel to search
    :param check_in: the date of the check_in
    :param check_out: the date of the check_out
    :param radius: the radius of the search
    :return: all possible rooms
    """
    check_in = datetime.strptime(check_in, "%Y-%m-%d")
    check_out = datetime.strptime(check_out, "%Y-%m-%d")
    room_ids = bepro_api.search_hotels("hotel", search_id, hotel_name, stars, check_in, check_out, radius)
    if room_ids:
        return room_ids
    else:
        return []


def get_rooms_prices_from_db(ids):
    """
    Get the possible room prices from the database
    :param ids: the ids of the rooms
    :return:the prices and check in date of the rooms
    """
    return sql_queries.select_room_price_by_id(ids)


def calculate_opportunities(room_prices, segment, last_year, arbitrage=50):
    """
    Calculate the opportunities for the given rooms
    :param room_prices: the prices of the rooms
    :param segment: the city of the hotel
    :param last_year: the year to camper the prices
    :param arbitrage: the profit we want to get
    :return:
    """
    opportunities = []
    month = get_the_check_in_month(room_prices[0])
    history_data = statisticall_information.get_statistically_information_for_segment(segment, month, last_year)
    print("history data", history_data)
    if len(history_data) != 0:
        history_price = statisticall_information.get_adr_for_month(history_data)
        for room in room_prices:
            print("price", room[1], "history_price", history_price)
            if room[1] + arbitrage <= history_price:
                opportunities.append(room[0])
    return opportunities


def get_the_check_in_month(check_in_room):
    """
    Extract the month from the given check in date
    :param check_in_room:the check in date to extract the month
    :return:the number month
    """
    return datetime.strptime(check_in_room[2], "%Y-%m-%d %H:%M:%S").month


def get_rooms_data_from_db(ids):
    """
    Get the data of room from the database
    :param ids: the ids of the rooms
    :return: all the date about the room
    """
    return sql_queries.select_data_of_opportunities(ids)


def select_hotel_data(room):
    """
    Get the all data of the hotel given an id from the database
    :param room: the id of the hotel
    :return: all the data of the hotel
    """
    hotel_id = room[1]
    return sql_queries.select_data_of_hotels_by_id(hotel_id)


def fill_hotel_data(data_hotel):
    """
    Fill the hotel data into the hotel object
    :param data_hotel: the data of the hotel
    :return: a hotel object
    """
    images = []
    for data in data_hotel:
        images.append(ResponseOpportunityImg(data[-1], data[-2]).body)
    item = ResponseOpportunityItem()
    item.validate_data(*data_hotel[0][:-2])
    item.add_images(images)
    return item.body


def fill_room_data(segment, data_rooms):
    """
    Fill the room data into the room object
    :param data_rooms: the data of the rooms
    :return: room objects
    """
    rooms = []
    for data in data_rooms:
        room = create_room(*data)
        room = opportunity_response_handler.calculate_profit(segment, room)
        rooms.append(room)
    return rooms


def create_room(room_id, price, desc, sys_code, check_in, check_out, nights, token,
                limit_date, remarks, meal_plan_code, meal_plan_desc):
    """
    Create a new room object
    :param room_id:the id of the room
    :param price: the price of the room
    :param desc: the description of the room
    :param sys_code: the system code of the room
    :param check_in: the check-in date of the room
    :param check_out: the check-out date of the room
    :param nights: the number of nights of the room
    :param token: the token of the room
    :param limit_date: the limit date of the room
    :param remarks: the remarks of the room
    :param meal_plan_code: the meal-plan code of the room
    :param meal_plan_desc: the meal-plan description of the room
    :return: a room object
    """
    body = {"RoomId": room_id, "Desc": desc, "Price": price, "Profit": 0, "SysCode": sys_code, "NumAdt": 2, "NumCnn": 0,
            "CnnAge": [], "CheckIn": check_in, "CheckOut": check_out, "Nights": nights, "BToken": token,
            "LimitDate": limit_date, "Remarks": remarks, "MetaData": {}}
    body["MetaData"]["Code"] = meal_plan_code
    body["MetaData"]["Desc"] = meal_plan_desc
    return body


def fill_response_data(item, rooms):
    """
    Fill and create the response data
    :param item: the data object of the hotel
    :param rooms: the data object of the rooms
    :return: the response data to return to the user
    """
    hotel = ResponseOpportunityHotel(item, rooms)
    return ResponseOpportunity([hotel.body]).body


def extract_data_from_sql_type(data):
    """
    Extract the data from the pysql type to list
    :param data: the sql data
    :return: the data by list type
    """
    return [list(item) for item in data]


def get_last_year():
    """
    Get the last year
    :return: the last year
    """
    return datetime.now().year - 1


def check_if_segment(city):
    """
    Check if the given city is a segment which is under surveillance
    :param city: the city to check
    :return: True if the city is under surveillance, False otherwise
    """
    search_settings = sql_queries.select_search_setting()
    for search_setting in search_settings:
        print(search_setting)
        if city in search_setting[1]:
            return True
    return False


def get_search_settings_id(city):
    search_settings = sql_queries.select_search_setting()
    for search_setting in search_settings:
        if city in search_setting[1]:
            return search_setting[0]


def check_correctness_of_the_hotel_name(hotel_name, hotel_name_to_check):
    """
    Check if the hotel name is correctly the same that given
    :param hotel_name: the given hotel name
    :param hotel_name_to_check: the database hotel name to check
    :return: True if the hotel name is correctly the same that given
    """
    return hotel_name == hotel_name_to_check


def bePro_search_one(hotel_name, stars, check_in, check_out, segment, radius, arbitrage):
    """
    The main function of the search one hotel date by bePro
    :param hotel_name: the hotel name to search
    :param stars: the number of stars of the hotel to search
    :param check_in: the check-in date
    :param check_out: the check-out date
    :param segment: the city of the hotel to search
    :param radius: the radius of the distance to search
    :param arbitrage: the profit of the hotel to search
    :return: all opportunities
    """
    try:
        print(hotel_name, stars, check_in, check_out)
        if not check_if_segment(segment):
            return "This city is not under surveillance"
        search_id = get_search_settings_id(segment)
        if hotel_name == "":
            rooms_ids = search_one_hotel(search_id, segment, stars, check_in, check_out, radius)
        else:
            hotel_name = hotel_name + " " + segment
            rooms_ids = search_one_hotel(search_id, hotel_name, stars, check_in, check_out, radius=1)
        print("room ids", rooms_ids)
        if rooms_ids:
            rooms_ids = list(set(rooms_ids))
            prices = get_rooms_prices_from_db(rooms_ids)
            last_year = get_last_year()
            segment = {"Id": search_id, "Name": segment}
            oppo = calculate_opportunities(prices, segment, last_year, arbitrage)
            print("oppo", len(oppo))
            if len(oppo) > 0:
                oppo_data = get_rooms_data_from_db(oppo)
                hotel_data = select_hotel_data(oppo_data[0])
                oppo_data = extract_data_from_sql_type(oppo_data)
                item = fill_hotel_data(hotel_data)
                if check_correctness_of_the_hotel_name(item.get("Name"), hotel_data[0][1]):
                    rooms = fill_room_data(segment, oppo_data)
                    print(rooms)
                    hotel = ResponseOpportunityHotel(item, rooms)
                    return {"Hotels": [hotel.body]}
                else:
                    "No opportunities exist for this hotel"
            else:
                return "No opportunities exist for these values"
        else:
            return "No information exists for these values"
    except Exception as e:
        return Exception(f"Something went wrong in 'bePro_search_one' function.\n {e}")
