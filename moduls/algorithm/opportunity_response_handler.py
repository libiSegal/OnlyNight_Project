from moduls.algorithm import opportunitiesFinder
from moduls.objects.response_opportunity_obj import ResponseOpportunityItem
from moduls.objects.response_opportunity_obj import ResponseOpportunityImg
from moduls.objects.response_opportunity_obj import ResponseOpportunityRoom
from moduls.objects.response_opportunity_obj import ResponseOpportunityHotel
from moduls.objects.response_opportunity_obj import ResponseOpportunity


def get_opportunities_response():
    res_hotels = []
    images = []
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
        res_rooms_list = []
        for index in rooms_indexes:
            data[index].pop(0)  # delete the hotel_id
            data[index].pop(1)    # delete the opportunity id
            res_rooms_list.append(ResponseOpportunityRoom(*data[index]).body)
            res_hotels.append(ResponseOpportunityHotel(res_item.body, res_rooms_list).body)
    return ResponseOpportunity(res_hotels).body


def extract_opportunities_from_db_type(opportunities):
    new_opportunities = []
    for opportunity in opportunities:
        row_data = []
        for data in opportunity:
            row_data.append(data)
        new_opportunities.append(row_data)
    return new_opportunities



