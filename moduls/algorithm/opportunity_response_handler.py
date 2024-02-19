from datetime import datetime
from dbConnections import sql_queries
from moduls.algorithm import opportunitiesFinder
from moduls.algorithm import statisticall_information as inflation


def get_opportunities_response():
    """
    This function gets the opportunities and organize them into a response object
    :return: The response object
    """
    res_hotels = []
    segments = get_segments()
    for segment in segments:
        print("segment", segment)
        opportunities_ids = opportunitiesFinder.search_opportunities(segment)
        if type(opportunities_ids) is not int:
            if len(opportunities_ids) > 0:
                opportunities_ids = list(set(opportunities_ids))
                opportunities = sql_queries.select_data_of_opportunities(opportunities_ids)
                print("opportunities", len(opportunities))
                hotels_ids = opportunitiesFinder.group_opportunities_hotels(opportunities)
                hotels = opportunitiesFinder.get_opportunities_hotels(hotels_ids)
                group_hotels = opportunitiesFinder.group_hotels_by_id(hotels)
                hotel_without_duplicates = opportunitiesFinder.remove_duplicate_data(group_hotels)
                opportunities_list = extract_opportunities_from_db_type(opportunities)
                hotels_rooms = opportunitiesFinder.match_room_hotel(hotel_without_duplicates, opportunities_list)
                for item in hotels_rooms.items():
                    data = item[1]  # item[0] = hotel id item[1] = hotel data
                    item_data_end = data.index("1") + 1
                    res_item = create_item(*data[0:item_data_end])
                    rooms_indexes = [index for index, item in enumerate(data) if isinstance(item, list)]
                    if type(rooms_indexes) is list:
                        if len(rooms_indexes) > 0:
                            rooms_indexes_start = rooms_indexes[0]
                            images = data[item_data_end:rooms_indexes_start]
                            res_images = handle_hotel_images(images)
                            res_item = add_images(res_item, res_images)
                            res_rooms_list = []
                            for index in rooms_indexes:
                                data[index].pop(1)  # delete the hotel id
                                room = create_room(*data[index])
                                room = calculate_profit(segment, room)
                                res_rooms_list.append(room)
                            unique_rooms = remove_duplicate_rooms(res_rooms_list)
                            hotel = create_hotel(res_item, unique_rooms)
                            res_hotels = check_hotel_is_exists(hotel, res_hotels)
    hotels = {"Hotels": res_hotels}
    return hotels


def get_segments():
    """
    Returns a list of segment objects from the database
    :return: A list of segments
    """
    segments_data = sql_queries.select_search_setting()
    return [{"Id": seg[0], "Name": seg[1].split(",")[0]} for seg in segments_data]


def extract_opportunities_from_db_type(opportunities):
    """
    Extract opportunities data room from the pyodbc type to list
    :param opportunities: the pyodbc data room to extract
    :return: A list of opportunities data
    """
    new_opportunities = []
    for opportunity in opportunities:
        row_data = []
        for data in opportunity:
            row_data.append(data)
        new_opportunities.append(row_data)
    return new_opportunities


def handle_hotel_images(hotel_images):
    """
    Function to process hotel images based on their dimensions and create new images if conditions are met.
    hotel_images: A list of image paths or URLs for the hotel.
    Returns: A list of new images created based on the conditions met.
    """
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
    """
    Creates an image object
    :param desc: the description of the image
    :param image_link: the url link to the image
    :return: the created image object
    """
    return {"Desc": desc, "ImageLink": image_link}


def create_item(*args):
    """
    Creates an item object  - hotel data
    :param args: the parameters of the item - hotel data
    :return: the created item object
    """
    body = {"Id": args[0], "Name": args[1], "Code": args[2], "Stars": args[3], "AddressInfo": {}, "Position": {}}
    body["AddressInfo"]["Address"] = args[4]
    body["AddressInfo"]["City"] = args[5]
    body["AddressInfo"]["Country"] = args[6]
    if len(args) == 10:
        body["AddressInfo"]["Phone"] = " "
        body["AddressInfo"]["Fax"] = " "
        body["Position"]["Latitude"] = args[7]
        body["Position"]["Longitude"] = args[8]
        body["Position"]["PIP"] = args[9]
    elif len(args) == 11:
        body["AddressInfo"]["Phone"] = args[7]
        body["AddressInfo"]["Fax"] = " "
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
    """
    Adds images to the hotel object
    :param hotel: the hotel object to be added images
    :param images: the images to be added to the hotel object
    :return: the updated hotel object
    """
    hotel["Images"] = images
    return hotel


def create_hotel(item, rooms):
    """
    Create a hotel object
    :param item: the hotel data
    :param rooms: a list of hotel rooms
    :return: the hotel object
    """
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
    body = {"RoomId": room_id, "Desc": desc, "Price": price, "Profit": 0, "SysCode": sys_code, "NumAdt": 2, "NumCnn": 0,
            "CnnAge": [], "CheckIn": check_in, "CheckOut": check_out, "Nights": nights, "BToken": token,
            "LimitDate": limit_date, "Remarks": remarks, "MetaData": {}}
    body["MetaData"]["Code"] = meal_plan_code
    body["MetaData"]["Desc"] = meal_plan_desc
    return body


def check_hotel_is_exists(hotel_to_check, hotel_list):
    """
    Check if a hotel exists in the list of hotels and update the rooms if it does.
    This function checks if a hotel with the same Name and Code as hotel_to_check exists in the hotel_list.
    If the hotel already exists, it updates the rooms of the existing hotel with new rooms from hotel_to_check.
    If the hotel does not exist in the list, it appends the hotel_to_check to the list.
    :param hotel_to_check: The hotel to check for existence and update rooms
    :param hotel_list: A list of hotels to search for the hotel_to_check
    :return: The updated hotel_list with the hotel added or rooms updated
    """
    flag = False
    if type(hotel_list) is list:
        if len(hotel_list) == 0:
            hotel_list.append(hotel_to_check)
            return hotel_list
        for hotel in hotel_list:
            if hotel.get("Item").get("Name") == hotel_to_check.get("Item").get("Name"):
                flag = True
        if not flag:
            hotel_list.append(hotel_to_check)
        return hotel_list


def check_room_in_hotel(room_to_check, rooms):
    """
    Check if a specific room exists in the list of rooms.
    This function takes a room to check and a list of rooms as input,
    and returns True if a room with the same RoomId as the room_to_check exists in the list of rooms,
    and False otherwise.
    :param room_to_check: The room to check for existence in the list of rooms
    :param rooms: A list of rooms to search for the room_to_check
    :return: True if the room_to_check exists in the rooms list, False otherwise
    """
    return any(room.get("RoomId") == room_to_check.get("RoomId") for room in rooms)


def remove_duplicate_rooms(room_list):
    """
    Removes duplicate rooms from a list of rooms by description value
    :param room_list: the list of rooms
    :return: the list of rooms without duplicate
    """
    room_desc = []
    for room in room_list:
        if room.get("Desc") not in room_desc:
            room_desc.append(room.get("Desc"))
        else:
            room_list.remove(room)
    return room_list


def calculate_profit(segment, room):
    """
    Calculates the profit for a room based on the price of the last year for the given segment
    :param segment: the city / country of the hotel
    :param room: the room to calculate the profit for
    :return: the room with the profit
    """
    check_in = room.get("CheckIn")
    date = datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S")
    data_for_month = inflation.get_statistically_information_for_segment(segment, date.month, date.year - 1)
    adr = inflation.get_adr_for_month(data_for_month)
    room["Profit"] = round(adr - room.get("Price"), 2)
    return room
