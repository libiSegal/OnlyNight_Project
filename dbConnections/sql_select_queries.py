from dbConnections import sql_db_connection as connection


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
