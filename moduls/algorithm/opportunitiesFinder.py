import itertools
from moduls.algorithm import statisticall_information
from dbConnections import sql_queries
from moduls.objects.opportunity_data_obj import OpportunityData


def search_opportunities(segment):
    opportunities = []
    arbitrage = 150
    rooms = statisticall_information.get_rooms()
    shorted_rooms_by_month = statisticall_information.short_rooms_by_month(rooms)
    for i in range(1, 13):
        history_data = statisticall_information.get_statistically_information_for_segment(segment, i, "2023")
        if len(history_data) != 0:
            history_price = statisticall_information.get_adr_for_month(history_data)
            for room in shorted_rooms_by_month[i - 1]:
                if room[1] + arbitrage < history_price:
                    opportunities.append(room[0])
    return opportunities


def grop_opportunities_hotels(opportunities_list):
    hotels_ids = []
    for k, g in itertools.groupby(opportunities_list, lambda x: x[1]):
        hotels_ids.append(k)
    return hotels_ids


def match_room_hotel(hotels, opportunities_list):
    hotels_and_rooms = {}
    for k, g in itertools.groupby(opportunities_list, lambda x: x[1]):
        for hotel in hotels:
            if k == hotel[0]:
                hotels_and_rooms[k] = list(hotel) + list(g)
    return hotels_and_rooms


def insert_opportunities_to_database(opportunities_list):
    for op in opportunities_list:
        opportunity = OpportunityData(op[0], op[1], op[2], op[3], op[4], op[5],
                                      op[6], op[7], op[8], op[10], op[9], op[11], op[12])
        sql_queries.insert_opportunities(opportunity)


def get_opportunities_from_db():
    return sql_queries.select_opportunities()


def get_opportunities_hotels(ids):
    return sql_queries.select_data_of_hotels_by_id(ids)


def grop_hotels_by_id(hotels_list):
    hotels = []
    for k, g in itertools.groupby(hotels_list, lambda x: x[0]):
        hotels.append(list(g))
    return hotels


def remove_duplicate_data(hotels_list):
    hotels_new_list = []
    for hotel in hotels_list:
        hotel_without_duplicate = []
        for data in hotel:
            for item in data:
                if item not in hotel_without_duplicate or item == "Room":
                    hotel_without_duplicate.append(item)
        hotels_new_list.append(hotel_without_duplicate)
    return hotels_new_list


# ids = search_opportunities("Berlin")
# data = basic_sql_queries.select_data_of_opportunities(ids)
# insert_opportunities_to_database(data)

