from dbConnections import sql_db_connection as connection


def inset_hotel_data(hotel_data):
    """
    Inset hotel data to database
    :param hotel_data: the data to inset
    :return: the new row id
    """
    insert_address = "dbo.insertAddress"
    address_values = (hotel_data.hotel_address, hotel_data.hotel_phone,
                      hotel_data.hotel_fax, hotel_data.hotel_city, hotel_data.hotel_country)
    address_id = connection.exec_stored_procedures(insert_address, address_values)[0]
    address_id = int(address_id[0])
    insert_position = "dbo.insertPosition"
    position_values = (hotel_data.hotel_latitude, hotel_data.hotel_longitude, hotel_data.hotel_pip)
    position_id = connection.exec_stored_procedures(insert_position, position_values)[0]
    position_id = int(position_id[0])
    insert_hotel = "dbo.insertHotel"
    hotel_values = (
        hotel_data.search_id, hotel_data.hotel_name, hotel_data.hotel_code, hotel_data.hotel_stars, address_id,
        position_id)
    hotel_id = connection.exec_stored_procedures(insert_hotel, hotel_values)
    return hotel_id


def insert_images(hotel_id, img, desc):
    """
    Inset hotels images to database
    :param hotel_id: the hotel id to insert
    :param img: the hotel image to insert
    :param desc: the img description to insert
    :return: None
    """
    insert_images_procedure = "dbo.insertImg"
    image_values = (hotel_id, img, desc)
    connection.exec_stored_procedures(insert_images_procedure, image_values)


def insert_room_data(room_data):
    """
    Inset room data to database
    :param room_data: the room data to insert
    :return: the new row id
    """
    insert_room = "dbo.insertRoom"
    room_values = (room_data.hotel_id, room_data.price, room_data.desc, room_data.sysCode, room_data.check_in,
                   room_data.check_out, room_data.nights, room_data.b_token, room_data.limit_date, room_data.remarks)
    room_id = connection.exec_stored_procedures(insert_room, room_values)[0]
    room_id = int(room_id[0])
    insert_mata_data = "dbo.insertMetadata"
    mata_values = (room_id, room_data.code, room_data.code_description)
    connection.exec_stored_procedures(insert_mata_data, mata_values)
    return room_id


def insert_cnn_ages(room_id, age):
    """
    insert child age into the database
    :param room_id: the room id to insert
    :param age: the age to insert
    :return: None
    """
    insert_cnn_ages_procedure = "dbo.insertCnnAge"
    cnn_age_values = (room_id, age)
    connection.exec_stored_procedures(insert_cnn_ages_procedure, cnn_age_values)


def insert_search_setting(stars, search_key):
    """
    insert search settings into the database
    :param stars: the number of stars to insert
    :param search_key: the city and country to insert
    :return: Nome
    """
    insert_search_settings_procedure = "dbo.insertSearchSetting"
    search_settings_values = (search_key, stars)
    connection.exec_stored_procedures(insert_search_settings_procedure, search_settings_values)


def insert_room_class(hotel_id, room_class, price, date):
    procedure = "dbo.insertNewRoomClass"
    room_class_values = (hotel_id, room_class, price, date)
    connection.exec_stored_procedures(procedure, room_class_values)


def update_room_class_prices(hotel_id, price):
    procedure = "dbo.updateRoomClassPrice"
    values = (hotel_id, price)
    connection.exec_stored_procedures(procedure, values)


def select_segment_id_of_hotel(hotel_id):
    procedure = "dbo.selectHotelSegment"
    return connection.exec_stored_procedures(procedure, hotel_id)


def select_hotels_name():
    """
    Retrieves a list of hotel names from the database.
    This function executes the 'dbo.selectHotelsNames' view in the database
    and collects the hotel names from the result set.
    :return: A list of hotel names
    """
    view_name = 'dbo.selectHotelsNames'
    names = []
    for row in connection.exec_views(view_name):
        names.append(row[0])
    return names


def select_search_setting():
    """
    select search settings from the database
    :return: the selected search settings
    """
    search_settings_view = "dbo.selectSearchSettings"
    return connection.exec_views(search_settings_view)


def select_room_prices_by_segment_id(seg_id):
    procedure_name = 'dbo.selectRoomsPricesById'
    return connection.exec_stored_procedures(procedure_name, seg_id)


def select_statistical_information_by_id(segment_id, year):
    procedure_name = 'dbo.selectStatisticalInformationById'
    values = (segment_id, year)
    return connection.exec_stored_procedures(procedure_name, values)


def select_data_of_opportunities(ids):
    """
    select data of the room - opportunities from the database
    :param ids: the ids of the room that they are opportunities
    :return: the data of the room by room
    """
    if ids is not None:
        ids_length = len(ids)
        res = []
        if ids_length > 0:
            db_data = connection.exec_query_select_rooms(ids)
            for row in db_data:
                res.append(row)
        return res


def select_data_of_hotels_by_id(ids):
    """
    select data from the hotels table by ids
    :param ids:the ids of the hotels to select
    :return:the hotels data
    """
    if isinstance(ids, int):
        ids = [ids]
    res = connection.exec_query_select_hotel_data(ids)
    if res:
        hotels = [row for row in res]
        return hotels
    else:
        return []


def select_room_price_by_id(ids):
    """
    select prices of rooms from database by ids
    :param ids: the ids of the rooms to select
    :return: the prices of the rooms
    """
    return connection.exec_query_select_room_prices_by_ids(ids)


def select_hotel_room_class(hotel_id):
    procedure_name = "dbo.selectHotelsRoomsClasses"
    return connection.exec_stored_procedures(procedure_name, hotel_id)


def select_statistically_information_by_month(month_number):
    """
    Select statistically information by month from the database
    :param month_number: The month number of the month to select the data
    :return: The information by month
    """
    month_view_map = {
        1: "dbo.selectJanuaryData",
        2: "dbo.selectFebruaryData",
        3: "dbo.selectMarchData",
        4: "dbo.selectAprilData",
        5: "dbo.selectMayData",
        6: "dbo.selectJuneData",
        7: "dbo.selectJulyData",
        8: "dbo.selectAugustData",
        9: "dbo.selectSeptemberData",
        10: "dbo.selectOctoberData",
        11: "dbo.selectNovemberData",
        12: "dbo.selectDecemberData"
    }

    view_name = month_view_map.get(month_number)
    if view_name:
        return connection.exec_views(view_name)
    else:
        raise ValueError("Month number is not in the range")
