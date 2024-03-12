from datetime import datetime
from dbConnections import sql_select_queries


def get_statistically_information_for_segment(segment, month, year):
    """
    This function select from database statistically information and screen out by month and year
    :param segment: segment to get statistically information for
    :param month: the month to get statistically information for
    :param year: the year to get statistically information for
    :return: statistically information on segment and month and year
    """
    statistically_information_table_for_segment = []
    statistically_information_table = sql_select_queries.select_statistically_information_by_month(month)
    for row in statistically_information_table:
        if row[4].split(',')[0] == segment.get("Name") and row[3] == year and row[5] == segment.get("Stars"):
            statistically_information_table_for_segment.append([row[0], row[1], row[2], row[3], row[4], row[5]])
    return statistically_information_table_for_segment


def get_adr_for_month(statistically_information):
    """
    Get adr value from statistically_information
    :param statistically_information: The statistically_information to get the adr value
    :return: The adr value from the statistically_information
    """
    if isinstance(statistically_information, list) and len(statistically_information) > 0:
        if isinstance(statistically_information[0], list):
            return statistically_information[0][0]
        return 0
    return 0


def get_revPar_for_month(statistically_information):
    """
    Get the revPar value for the statistical data
    :param statistically_information: The statistical data to get the revPar value for
    :return: The revPar value for the statistical data
    """
    if isinstance(statistically_information, list) and isinstance(statistically_information[0], list):
        return statistically_information[0][1]
    return 0


def get_occupancy_for_month(statistically_information):
    """
    Get the occupancy value from the statistical data
    :param statistically_information: The statistical data to get the occupancy for
    :return: the occupancy value
    """
    if isinstance(statistically_information, list) and isinstance(statistically_information[0], list):
        return statistically_information[0][2]
    return 0


def get_rooms_prices(segment_id):
    """
    This function takes a segment_id and returns the rooms prices for that segment
    :param segment_id: The id of the segment to get the prices for rooms
    :return: The rooms prices for that segment
    """
    return sql_select_queries.select_room_prices_by_segment_id(segment_id)


def short_rooms_by_month(rooms):
    """
    This function takes a list of rooms and returns a list of short rooms by check in month
    :param rooms: A list of rooms
    :return: A list of short rooms by check in month
    """
    months = [[] for _ in range(12)]
    for room in rooms:
        check_in = room[2]
        date = datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S")
        month_index = date.month - 1
        months[month_index].append(room)
    return months
