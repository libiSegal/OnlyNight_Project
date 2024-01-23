from dbConnections import basic_sql_queries as sql_queries
from moduls.objects.hotel_data_obj import HotelData
from moduls.objects.room_data_obj import RoomData


def handle_data_hotel(hotel):
    item = hotel.get('Item')
    address_info = hotel.get('AddressInfo')
    position = hotel.get('Position')
    images = hotel.get('Images')
    hotel_data = HotelData(item.get('UniqueName'), item.get('Code'), item.get('Star'), address_info.get('Address'),
                           address_info.get('Phone'), address_info.get('Fax'), address_info.get('City'),
                           address_info.get('Country'), position.get('Latitude'),
                           position.get('Longitude'), position.get('PIP'))

    hotel_id = sql_queries.inset_hotel_data(hotel_data)[0]
    hotel_id = int(hotel_id)
    for img in images:
        sql_queries.insert_images(hotel_id, img.get('ImageLink'), img.get('Desc'))

    rooms = hotel.get("RoomClasses")
    handle_room_data(hotel_id, rooms)


def handle_room_data(hotel_id, rooms):
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
        room_id = sql_queries.insert_room_data(room_data)
        if room_id is not None:
            room_id = int(room_id[0])
        if hotel_rooms.get('SysCode')[3] != 0:
            pass



