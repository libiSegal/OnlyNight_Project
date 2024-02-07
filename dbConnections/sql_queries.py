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


def insert_opportunities(opportunity_data):
    """
    insert opportunities into the database
    :param opportunity_data: the opportunity data to insert
    :return: None
    """
    procedure_name = 'dbo.insertOpportunities'
    oppo_values = (opportunity_data.room_id, opportunity_data.hotel_id, opportunity_data.price, opportunity_data.desc,
                   opportunity_data.sysCode, opportunity_data.check_in, opportunity_data.check_out,
                   opportunity_data.nights, opportunity_data.b_token, opportunity_data.limit_date,
                   opportunity_data.remarks, opportunity_data.code, opportunity_data.code_description)
    connection.exec_stored_procedures(procedure_name, oppo_values)


def select_hotels_name():
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


def select_opportunities():
    """
    select opportunities from the opportunities table in database
    :return: the data of the opportunities
    """
    view_name = 'dbo.selectOpportunities'
    res = connection.exec_views(view_name)
    opportunities = [row for row in res]
    return opportunities


def select_data_of_hotels_by_id(ids):
    """
    select data from the hotels table by ids
    :param ids:the ids of the hotels to select
    :return:the hotels data
    """
    res = connection.exec_query_select_hotel_data(ids)
    if res:
        hotels = [row for row in res]
        return hotels


def select_number_of_rooms():
    procedure_name = "dbo.selectNumberOfRooms"
    res = connection.exec_stored_procedures(procedure_name, "")
    return int(res[0])


def select_first_room_id():
    procedure_name = "dbo.selectFirstRoomId"
    res = connection.exec_stored_procedures(procedure_name, "")
    return int(res[0])


def selectRooms(start, end):
    func_name = "dbo.selectRooms"
    return connection.exec_functions(func_name, start, end)


def selectRoomsPrices():
    """
    select prices of rooms from database
    :return: a list of room prices and ids
    """
    view_name = "dbo.selectRoomsPrices"
    return connection.exec_views(view_name).fetchall()


def select_room_price_by_id(ids):
    """
    select prices of rooms from database by ids
    :param ids: the ids of the rooms to select
    :return: the prices of the rooms
    """
    return connection.exec_query_select_room_prices_by_ids(ids)


def select_statistically_information_by_month(month_number):
    """
    select statistically information by month from database
    :param month_number: the month number of the month to select the data
    :return: the  information by month
    """
    view_name = ""
    match month_number:
        case 1:
            view_name = "dbo.selectJanuaryData"
        case 2:
            view_name = "dbo.selectFebruaryData"
        case 3:
            view_name = "dbo.selectMarchData"
        case 4:
            view_name = "dbo.selectAprilData"
        case 5:
            view_name = "dbo.selectMayData"
        case 6:
            view_name = "dbo.selectJuneData"
        case 7:
            view_name = "dbo.selectJulyData"
        case 8:
            view_name = "dbo.selectAugustData"
        case 9:
            view_name = "dbo.selectSeptemberData"
        case 10:
            view_name = "dbo.selectOctoberData"
        case 11:
            view_name = "dbo.selectNovemberData"
        case 12:
            view_name = "dbo.selectDecemberData"
        case _:
            return ValueError("Month number is not in the range")
    return connection.exec_views(view_name)
