from moduls.beProApi import search_hotels_data_functions_handler as search_hotels_data
from moduls.beProApi import search_hotels_functions as search_htl
from moduls.beProApi import hotels_data_handler as hotel_handler
from moduls.jsonHandler import json_reader as jdr

URL = 'https://pub_srv.beprotravel.net/BePro'


def search_hotels(search_key, geo_code, stars, check_in, check_out, num_adults, num_children, children_age):
    country_name = search_hotels_data.get_country_name(search_key)
    country_code = search_hotels_data.convert_country_name_to_code(country_name)
    nights = search_hotels_data.calculate_number_of_nights(check_in, check_out)
    check_in = search_hotels_data.change_dates_format(check_in)
    rooms = search_hotels_data.build_room(num_adults, num_children, children_age)
    unique_key = search_htl.search_post_request(search_key, country_code, geo_code, check_in, nights, rooms, stars)
    urls_hotels = search_htl.get_the_hotels_details(unique_key)
    search_htl.download_hotels_data(urls_hotels)
    insert_hotels_data_into_db()
    jdr.delete_jsons_files('files')


def insert_hotels_data_into_db():
    print("Inserting hotels data...")
    hotels = jdr.get_clean_data('files')
    print(hotels)
    for hotel in hotels:
        hotel_handler.handle_data_hotel(hotel)
