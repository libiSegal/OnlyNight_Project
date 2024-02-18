from dbConnections import sql_queries


def check_room_class_exist(room_class, room_classes):
    if len(room_classes) == 0:
        return False
    for room in room_classes:
        if room == room_class:
            return True
    return True


def insert_new_room_class(hotel_id, room_class, price):
    sql_queries.insert_room_class(hotel_id, room_class, price)


def get_room_classes_for_hotel(hotel_id):
    return sql_queries.select_room_class(hotel_id)


def main(hotel_id, room):
    hotel_classes = get_room_classes_for_hotel(hotel_id)
    print(room)
    if not check_room_class_exist(room.desc, hotel_classes):
        insert_new_room_class(hotel_id, room.desc, room.price)
    else:
        pass


