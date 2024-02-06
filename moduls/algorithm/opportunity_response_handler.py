from moduls.algorithm import opportunitiesFinder
from moduls.objects.response_opportunity_obj import ResponseOpportunityItem
from moduls.objects.response_opportunity_obj import ResponseOpportunityImg
from moduls.objects.response_opportunity_obj import ResponseOpportunityRoom
from moduls.objects.response_opportunity_obj import ResponseOpportunityHotel
from moduls.objects.response_opportunity_obj import ResponseOpportunity


def get_opportunities_response():
    res_hotels = []
    opportunities = opportunitiesFinder.get_opportunities_from_db()
    hotels_ids = opportunitiesFinder.grop_opportunities_hotels(opportunities)
    hotels = opportunitiesFinder.get_opportunities_hotels(hotels_ids)
    grop_hotels = opportunitiesFinder.grop_hotels_by_id(hotels)
    hotel_without_duplicates = opportunitiesFinder.remove_duplicate_data(grop_hotels)
    opportunities_list = extract_opportunities_from_db_type(opportunities)
    hotels_rooms = opportunitiesFinder.match_room_hotel(hotel_without_duplicates, opportunities_list)
    for item in hotels_rooms.items():
        data = item[1]  # item[0] = hotel id item[1] = hotel data
        item_data_end = data.index("1") + 1
        res_item = ResponseOpportunityItem()
        res_item.validate_data(*data[0:item_data_end])
        rooms_indexes = [index for index, item in enumerate(data) if isinstance(item, list)]
        rooms_indexes_start = rooms_indexes[0]
        images = data[item_data_end:rooms_indexes_start]
        res_images = handle_hotel_images(images)
        res_item.add_images(res_images)
        res_rooms_list = []
        for index in rooms_indexes:
            data[index].pop(0)  # delete the hotel_id
            data[index].pop(1)  # delete the opportunity id
            room = ResponseOpportunityRoom()
            room.fill_obj(*data[index])
            desc = data[index][2]
            room.add_desc(desc)
            res_rooms_list.append(room.body)
        hotel = ResponseOpportunityHotel(res_item.body, res_rooms_list).body
        res_hotels.append(hotel)
    return ResponseOpportunity(res_hotels).body


def extract_opportunities_from_db_type(opportunities):
    new_opportunities = []
    for opportunity in opportunities:
        row_data = []
        for data in opportunity:
            row_data.append(data)
        new_opportunities.append(row_data)
    return new_opportunities


def handle_hotel_images(hotel_images):
    images = []
    if len(hotel_images) % 2 == 0:
        if len(hotel_images[0]) < len(hotel_images[1]):
            for i in range(len(hotel_images) - 1):
                if len(hotel_images[i]) < len(hotel_images[i+1]):
                    images.append(ResponseOpportunityImg(hotel_images[i], hotel_images[i + 1]).body)

    else:
        for i in range(len(hotel_images) - 1):
            if len(hotel_images[i]) > len(hotel_images[i + 1]):
                images.append(ResponseOpportunityImg("", hotel_images[i]).body)
            else:
                images.append(ResponseOpportunityImg(" ", hotel_images[i + 1]).body)
    return images


get_opportunities_response()