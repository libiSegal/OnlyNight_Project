from dbConnections import sql_queries
from datetime import datetime


def get_statistically_information_for_segment(segment, month, year):
    print("get_statistically_information_for_segment called", month)
    statistically_information_table = sql_queries.select_statistically_information_by_month(month)
    statistically_information_table_for_segment = []
    for row in statistically_information_table:
        if row[4] == segment.get("Name") and row[3] == year:
            statistically_information_table_for_segment.append([row[0], row[1], row[2], row[3], row[4], row[5]])
    return statistically_information_table_for_segment


def get_adr_for_month(statistically_information):
    return statistically_information[0][0]


def get_revPar_for_month(statistically_information):
    return statistically_information[0][1]


def get_occupancy_for_month(statistically_information):
    return statistically_information[0][2]


def get_rooms(segment_id):
    return sql_queries.select_room_prices_by_segment_id(segment_id)


def short_rooms_by_month(rooms):
    months = [[] for _ in range(12)]  # List comprehension to create empty lists for each month
    for room in rooms:
        check_in = room[2]
        date = datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S")
        month_index = date.month - 1  # Adjust month index to start from 0
        months[month_index].append(room)
    print("february", months[1])
    print("december", months[11])
    return months
