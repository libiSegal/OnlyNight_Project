from dbConnections import sql_queries
from datetime import datetime


def get_statistically_information_for_segment(segment, month, year):
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
    january = february = march = april = may = june = july = august = september = october = november = december = []
    for room in rooms:
        check_in = room[2]
        date = datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S")
        match date.month:
            case 1:
                january.append(room)
            case 2:
                february.append(room)
            case 3:
                march.append(room)
            case 4:
                april.append(room)
            case 5:
                may.append(room)
            case 6:
                june.append(room)
            case 7:
                july.append(room)
            case 8:
                august.append(room)
            case 9:
                september.append(room)
            case 10:
                october.append(room)
            case 11:
                november.append(room)
            case 12:
                december.append(room)
    return [january, february, march, april, may, june, july, august, september, october, november, december]



