import datetime
import itertools
from dbConnections import sql_queries
from moduls.algorithm import statisticall_information


def search_opportunities(segment):
    """
    This function takes a segment and returns a list of opportunities found in segment
    :param segment: The segment to search for opportunities
    :return: A list of opportunities ids
    """
    opportunities = []
    arbitrage = 150
    rooms = statisticall_information.get_rooms_prices(segment.get("Id"))
    shorted_rooms_by_month = statisticall_information.short_rooms_by_month(rooms)
    for i in range(1, 13):
        history_data = statisticall_information.get_statistically_information_for_segment(segment, i,
                                                                                          datetime.date.today().year - 1)
        if len(history_data) != 0:
            history_price = statisticall_information.get_adr_for_month(history_data)
            for room in shorted_rooms_by_month[i - 1]:
                if room[1] + arbitrage < history_price:  # room[1] == room price
                    opportunities.append(room[0])
    return opportunities


def group_opportunities_hotels(opportunities_list):
    """
    This function takes a list of opportunities and groups them into one list by ids
    :param opportunities_list: A list of opportunities
    :return: A list of the opportunities grouped by id
    """
    hotels_ids = []
    for k, g in itertools.groupby(opportunities_list, lambda x: x[1]):
        hotels_ids.append(k)
    return hotels_ids


def match_room_hotel(hotels, opportunities_list):
    """
    This function takes a list of rooms and matches them to hotel based on ids
    :param hotels: A list of hotels
    :param opportunities_list: A list of opportunities - rooms
    :return: The list of opportunities sorted by hotels
    """
    hotels_and_rooms = {}
    for k, g in itertools.groupby(opportunities_list, lambda x: x[1]):
        for hotel in hotels:
            if k == hotel[0]:
                hotels_and_rooms[k] = list(hotel) + list(g)
    return hotels_and_rooms


def get_opportunities_hotels(ids):
    """
    Select the data of the opportunities hotels from database by id
    :param ids: The hotels ids
    :return: The opportunities hotels data from the database
    """
    return sql_queries.select_data_of_hotels_by_id(ids)


def group_hotels_by_id(hotels_list):
    """
    Group hotels by their ids
    :param hotels_list: The list of hotels
    :return: The list of grouped hotels
    """
    hotels = []
    for k, g in itertools.groupby(hotels_list, lambda x: x[0]):
        hotels.append(list(g))
    return hotels


def remove_duplicate_data(hotels_list):
    """
    Removes duplicate hotel data from hotel data from list
    :param hotels_list: The list of hotel data
    :return: A list of hotel data without duplicates
    """
    hotels_new_list = []
    for hotel in hotels_list:
        hotel_without_duplicate = []
        for data in hotel:
            for item in data:
                if item not in hotel_without_duplicate or item == "Room":
                    hotel_without_duplicate.append(item)
        hotels_new_list.append(hotel_without_duplicate)
    return hotels_new_list
