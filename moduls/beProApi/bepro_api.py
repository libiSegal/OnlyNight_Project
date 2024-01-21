from moduls.beProApi import data_handler
from moduls.beProApi import search_hotels_functions as search_htl

URL = 'https://pub_srv.beprotravel.net/BePro'


def search_hotels(search_key, geo_code, stars, check_in, check_out, num_adults, num_children, children_age):
    country_name = data_handler.get_country_name(search_key)
    country_code = data_handler.convert_country_name_to_code(country_name)
    nights = data_handler.calculate_number_of_nights(check_in, check_out)
    check_in = data_handler.change_dates_format(check_in)
    rooms = data_handler.build_room(num_adults, num_children, children_age)
    unique_key = search_htl.search_post_request(search_key, country_code, geo_code, check_in, nights, rooms, stars)
    urls_hotels = search_htl.get_the_hotels_details(unique_key)
    search_htl.download_hotels_data(urls_hotels)

# search_hotels("Berlin, Germany",
#               {
#                   "Latitude": "52.52000659999999",
#                   "Longitude": "13.404954",
#                   "PIP": "N"
#               },
#               "2024/02/01",
#               "2024/02/02",
#               [{
#                   "SysRoomCode": "O2A0C",
#                   "NumRoom": 1,
#                   "NumCots": 0,
#                   "NumPax": 2,
#                   "NumAdt": 2,
#                   "NumCnn": 0,
#                   "CnnAge1": 0,
#                   "CnnAge2": 0,
#                   "CnnAge3": 0,
#                   "CnnAge4": 0
#               }],
#               4
#               )
