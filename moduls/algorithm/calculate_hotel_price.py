import re
import itertools
from datetime import datetime
from dbConnections import sql_queries


def remove_special_chars(input_string):
    """Remove special characters from the input string."""
    return re.sub(r'[^a-zA-Z0-9\s]', '', input_string)


def check_room_class_exist(room_class, room_classes):
    """Check if room class exists in the list of room classes."""
    room_class = remove_special_chars(room_class)
    if not room_classes:
        return False
    for room in room_classes:
        db_room_class = remove_special_chars(room[1])
        if db_room_class == room_class:
            return True
    return False


def check_cancellation_policy(room):
    """Check if date of cancellation policy is effect."""
    print(room.limit_date)
    limit_date = datetime.strptime(room.limit_date, "%Y-%m-%d %H:%M:%S")
    if limit_date is None:
        return False
    if limit_date <= datetime.today():
        return False
    return True


def insert_new_room_class(hotel_id, room_class, price, date):
    """Insert a new room class into the database."""
    room_class = remove_special_chars(room_class)
    sql_queries.insert_room_class(hotel_id, room_class, price, date)


def update_room_class_price(hotel_id, price):
    """Update the room class price in the database."""
    sql_queries.update_room_class_prices(hotel_id, price)


def get_room_classes_for_hotel(hotel_id):
    """Retrieve room classes for a specific hotel from the database."""
    return sql_queries.select_hotel_room_class(hotel_id)


def get_room_class_price(r_class, hotel_classes):
    """Get the price of a specific room class."""
    for hotel in hotel_classes:
        if hotel[1] == r_class:
            return hotel[0], hotel[2]  # hotel[0] = id , hotel[1] = price
    return 0, 0


def calculate_hotel_room_class_price(hotel_id, room):
    """Calculate and update the room class price for a hotel."""
    hotel_classes = get_room_classes_for_hotel(hotel_id)
    if check_cancellation_policy(room) and not check_room_class_exist(room.desc, hotel_classes):
        insert_new_room_class(hotel_id, room.desc, room.price, room.check_in)
    else:
        old_id, old_price = get_room_class_price(room.desc, hotel_classes)
        if old_price != 0 and room.price < old_price:
            update_room_class_price(old_id, room.price)


def grouped_hotel_class_by_date(hotel_classes):
    """Group hotel classes by check in date"""
    grouped_hotel_classes = {}

    for k, g in itertools.groupby(hotel_classes, lambda x: x[3]):
        grouped_hotel_classes[k] = [{"RoomClass": item[1], "Price": item[2]} for item in g]

    return grouped_hotel_classes


def short_info_by_month(info):
    """Short info by month and return an array of short info - adr for month"""
    shorted_info = [0] * 12

    for item in info:
        shorted_info[item[0] - 1] = item[1]

    return shorted_info


def get_history_prices(hotel_id):
    """Get hotel monthly prices for last year"""
    segment_id = sql_queries.select_segment_id_of_hotel(hotel_id)
    info = sql_queries.select_statistical_information_by_id(segment_id[0][0], datetime.today().year - 1)
    return short_info_by_month(info)


def get_hotel_room_classes(hotel_id):
    """Get hotel room classes for a specific hotel."""
    hotel_classes = get_room_classes_for_hotel(hotel_id)
    current_price_hotel = grouped_hotel_class_by_date(hotel_classes)
    history_price_hotel = get_history_prices(hotel_id)
    return {"CurrentPriceHotel": current_price_hotel, "HistoryPriceHotel": history_price_hotel}
