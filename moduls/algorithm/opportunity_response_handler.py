from moduls.algorithm import opportunitiesFinder
from dbConnections import sql_queries
# from moduls.objects.response_opportunity_obj import ResponseOpportunityImg
# from moduls.objects.response_opportunity_obj import ResponseOpportunityRoom
# from moduls.objects.response_opportunity_obj import ResponseOpportunityHotel
from moduls.objects.response_opportunity_obj import ResponseOpportunity


def get_opportunities_response():
    num = 0
    res_hotels = []
    # opportunities = opportunitiesFinder.get_opportunities_from_db()
    opportunities_ids = opportunitiesFinder.search_opportunities("Berlin")
    opportunities = sql_queries.select_data_of_opportunities(opportunities_ids)
    hotels_ids = opportunitiesFinder.grop_opportunities_hotels(opportunities)
    hotels = opportunitiesFinder.get_opportunities_hotels(hotels_ids)
    grop_hotels = opportunitiesFinder.grop_hotels_by_id(hotels)
    hotel_without_duplicates = opportunitiesFinder.remove_duplicate_data(grop_hotels)
    opportunities_list = extract_opportunities_from_db_type(opportunities)
    hotels_rooms = opportunitiesFinder.match_room_hotel(hotel_without_duplicates, opportunities_list)
    for item in hotels_rooms.items():
        data = item[1]  # item[0] = hotel id item[1] = hotel data
        item_data_end = data.index("1") + 1
        res_item = create_item(*data[0:item_data_end])
        num +=1
        rooms_indexes = [index for index, item in enumerate(data) if isinstance(item, list)]
        rooms_indexes_start = rooms_indexes[0]
        images = data[item_data_end:rooms_indexes_start]
        res_images = handle_hotel_images(images)
        res_item = add_images(res_item, res_images)
        res_rooms_list = []
        for index in rooms_indexes:
            data[index].pop(1)  # delete the hotel id
            room = create_room(*data[index])
            res_rooms_list.append(room)
        hotel = create_hotel(res_item, res_rooms_list)
        res_hotels.append(hotel)
    print("num", num)
    return ResponseOpportunity(res_hotels).body


def extract_opportunities_from_db_type(opportunities):
    new_opportunities = []
    for opportunity in opportunities:
        row_data = []
        for data in opportunity:
            row_data.append(data)
        new_opportunities.append(row_data)
    return new_opportunities


def handle_hotel_images(hotel_images):
    images = []
    if len(hotel_images) % 2 == 0:
        if len(hotel_images[0]) < len(hotel_images[1]):
            for i in range(len(hotel_images) - 1):
                if len(hotel_images[i]) < len(hotel_images[i + 1]):
                    images.append(create_img(hotel_images[i], hotel_images[i + 1]))

    else:
        for i in range(len(hotel_images) - 1):
            if len(hotel_images[i]) > len(hotel_images[i + 1]):
                images.append(create_img("", hotel_images[i]))
            else:
                images.append(create_img(" ", hotel_images[i + 1]))
    return images


def create_img(desc, image_link):
    return {"Desc": desc, "ImageLink": image_link}


def create_item(*args):
    body = {"Id": args[0], "Name": args[1], "Code": args[2], "Stars": args[3], "AddressInfo": {}, "Position": {}}
    body["AddressInfo"]["Address"] = args[4]
    body["AddressInfo"]["City"] = args[5]
    body["AddressInfo"]["Country"] = args[6]
    if len(args) == 10:
        body["AddressInfo"]["Phone"] = type[str]
        body["AddressInfo"]["Fax"] = type[str]
        body["Position"]["Latitude"] = args[7]
        body["Position"]["Longitude"] = args[8]
        body["Position"]["PIP"] = args[9]
    elif len(args) == 11:
        body["AddressInfo"]["Phone"] = args[7]
        body["AddressInfo"]["Fax"] = type[str]
        body["Position"]["Latitude"] = args[8]
        body["Position"]["Longitude"] = args[9]
        body["Position"]["PIP"] = args[10]
    else:
        body["AddressInfo"]["Phone"] = args[7]
        body["AddressInfo"]["Fax"] = args[8]
        body["Position"]["Latitude"] = args[9]
        body["Position"]["Longitude"] = args[10]
        body["Position"]["PIP"] = args[11]
    body["Images"] = []
    return body


def add_images(hotel, images):
    hotel["Images"] = images
    return hotel


def create_hotel(item, rooms):
    return {"Item": item, "Rooms": rooms}


def create_room(room_id, price, desc, sys_code, check_in, check_out, nights, token,
                limit_date, remarks, meal_plan_code, meal_plan_desc, ):
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
    body = {"RoomId": room_id, "Desc": desc, "Price": price, "SysCode": sys_code, "NumAdt": 2, "NumCnn": 0,
            "CnnAge": [], "CheckIn": check_in, "CheckOut": check_out, "Nights": nights, "BToken": token,
            "LimitDate": limit_date, "Remarks": remarks, "MetaData": {}}
    body["MetaData"]["Code"] = meal_plan_code
    body["MetaData"]["Desc"] = meal_plan_desc
    return body
