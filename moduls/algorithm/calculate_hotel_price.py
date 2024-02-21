import re
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


def insert_new_room_class(hotel_id, room_class, price):
    """Insert a new room class into the database."""
    room_class = remove_special_chars(room_class)
    sql_queries.insert_room_class(hotel_id, room_class, price)


def update_room_class_price(hotel_id, price):
    """Update the room class price in the database."""
    sql_queries.update_room_class_prices(hotel_id, price)


def get_room_classes_for_hotel(hotel_id):
    """Retrieve room classes for a specific hotel from the database."""
    return sql_queries.select_room_class(hotel_id)


def get_room_class_price(r_class, hotel_classes):
    """Get the price of a specific room class."""
    for hotel in hotel_classes:
        if hotel[1] == r_class:
            return hotel[0], hotel[2]  # hotel[0] = id , hotel[1] = price
    return 0, 0


def calculate_hotel_room_class_price(hotel_id, room):
    """Calculate and update the room class price for a hotel."""
    hotel_classes = get_room_classes_for_hotel(hotel_id)
    if not check_room_class_exist(room.desc, hotel_classes):
        insert_new_room_class(hotel_id, room.desc, room.price)
    else:
        old_id, old_price = get_room_class_price(room.desc, hotel_classes)
        if old_price != 0 and room.price < old_price:
            update_room_class_price(old_id, room.pric)
