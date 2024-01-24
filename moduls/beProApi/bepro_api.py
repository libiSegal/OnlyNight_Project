from moduls import google_maps_api
from moduls.beProApi import search_hotels_data_functions_handler as search_hotels_data
from moduls.beProApi import search_hotels_functions as search_htl
from moduls.beProApi import hotels_data_handler as hotel_handler
from moduls.jsonHandler import json_reader as jdr
from moduls.beProApi import bepro_definitions as defn


URL = 'https://pub_srv.beprotravel.net/BePro'


def search_hotels(search_key, stars, check_in, check_out):
    """
    this function is used to search hotels by bePro api and inserted the response into the database
    :param search_key: the city and country of the hotel you want to search
    :param stars: the number of stars of the hotel you want to search
    :param check_in: the date of the checkin
    :param check_out: the date of the checkOut
    :return:None
    """
    geo_code = google_maps_api.get_geo_code(search_key)
    country_name = search_hotels_data.get_country_name(search_key)
    country_code = search_hotels_data.convert_country_name_to_code(country_name)
    nights = search_hotels_data.calculate_number_of_nights(check_in, check_out)
    rooms = search_hotels_data.build_room(defn.numbers_adults, defn.numbers_children, defn.cnn_age)
    check_in = str(check_in)
    unique_key = search_htl.search_post_request(search_key, country_code, geo_code, check_in, nights, rooms, stars)
    urls_hotels = search_htl.get_the_hotels_details(unique_key)
    search_htl.download_hotels_data(urls_hotels)
    insert_hotels_data_into_db()
    jdr.delete_jsons_files('files')


def insert_hotels_data_into_db():
    """
    the function take the hotels from the files directory and insert them into the database
    :return: None
    """
    hotels = jdr.get_clean_data(r'files')
    for hotel in hotels:
        hotel_handler.handle_data_hotel(hotel)
