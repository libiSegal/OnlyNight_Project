from dbConnections import sql_queries


def check_room_class_exist(room_class, room_classes):
    room_class = room_class.replace("(", "").replace(")", "")
    if len(room_classes) == 0:
        return False
    for room in room_classes:
        if room[1] == room_class:
            return True
    return False


def insert_new_room_class(hotel_id, room_class, price):
    sql_queries.insert_room_class(hotel_id, room_class, price)


def get_room_classes_for_hotel(hotel_id):
    return sql_queries.select_room_class(hotel_id)


def get_room_class_price(r_class, hotel_classes):
    for hotel in hotel_classes:
        if hotel[1] == r_class:
            return hotel[2]


def main(hotel_id, room):
    hotel_classes = get_room_classes_for_hotel(hotel_id)
    if not check_room_class_exist(room.desc, hotel_classes):
        insert_new_room_class(hotel_id, room.desc, room.price)
    old_price = get_room_class_price(room.desc, hotel_classes)
    if old_price is not None:
        if room.price < old_price:
            pass
