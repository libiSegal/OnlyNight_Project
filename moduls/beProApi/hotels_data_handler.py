from moduls import xsl_writer
from moduls.objects.room_data_obj import RoomData
from moduls.algorithm import calculate_hotel_price
from moduls.objects.hotel_data_obj import HotelData
from dbConnections import sql_insert_queries


def handle_data_hotel(search_id, hotel):
    """
    Make ready the date from beProApi to insert into the db
    :param search_id: The segment id of the hotel
    :param hotel: the data to be inserted
    :return: None
    """
    item = hotel.get('Item')
    address_info = hotel.get('AddressInfo')
    position = hotel.get('Position')
    images = hotel.get('Images')
    hotel_data = HotelData(search_id, item.get('UniqueName'), item.get('Code'), item.get('Star'),
                           address_info.get('Address'),
                           address_info.get('Phone'), address_info.get('Fax'), address_info.get('City'),
                           address_info.get('Country'), position.get('Latitude'),
                           position.get('Longitude'), position.get('PIP'))
    print("bePro hotel name", item.get('UniqueName'))
    hotel_id = sql_insert_queries.inset_hotel_data(hotel_data)[0]
    hotel_id = int(hotel_id[0])
    if type(images) is list and len(images) > 3:
        images = images[:3]
        print("images", len(images))
        for img in images:
            sql_insert_queries.insert_images(hotel_id, img.get('ImageLink'), img.get('Desc'))
    rooms = hotel.get("RoomClasses")
    print("bePro hotel rooms", len(rooms))
    xsl_writer.insert_rooms_into_excel([[item.get('UniqueName')]])
    return handle_room_data(hotel_id, rooms)


def handle_room_data(hotel_id, rooms):
    """
    Make ready the date room from beProApi to insert into the db
    :param hotel_id: the id of the hotel
    :param rooms: the room data to be inserted
    :return: None
    """
    rooms_ids = []
    list_for_xsl = []
    for room in rooms:
        hotel_rooms = room.get('HotelRooms')[0]
        code = room.get('Board').get('Basis').get('Code')
        desc = room.get('Board').get('Basis').get('Desc')
        limit_date = room.get("CXL").get('LimitDate')
        if limit_date is None:
            limit_date = ""
        room_data = RoomData(hotel_id, room.get('Price').get('USD'), hotel_rooms.get('Desc'),
                             hotel_rooms.get('SysCode'), room.get('CheckIn'),
                             room.get('CheckOut'),
                             room.get('Nights'), hotel_rooms.get('BToken'),
                             room.get('Remarks'),
                             limit_date, code, desc)
        # the new calculate func is here
        calculate_hotel_price.calculate_hotel_room_class_price(hotel_id, room_data)
        list_for_xsl.append([room.get('Price').get('USD'), hotel_rooms.get('Desc'),
                             hotel_rooms.get('SysCode'), room.get('CheckIn'),
                             room.get('CheckOut'),
                             room.get('Nights'), hotel_rooms.get('BToken'),
                             room.get('Remarks'),
                             limit_date, code, desc])
        room_id = sql_insert_queries.insert_room_data(room_data)
        if room_id is not None:
            room_id = int(room_id)
            rooms_ids.append(room_id)
        if hotel_rooms.get('SysCode') is not None and len(hotel_rooms.get('SysCode')) > 3:
            if hotel_rooms.get('SysCode')[3] != 0:
                pass
    xsl_writer.insert_rooms_into_excel(list_for_xsl)
    return rooms_ids
