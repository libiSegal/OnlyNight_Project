import data_handler
import search_hotels_functions as search

URL = 'https://pub_srv.beprotravel.net/BePro'


def search_hotels(search_key, geo_code, check_in, check_out, rooms, stars):
    country_name = data_handler.get_country_name(search_key)
    country_code = data_handler.convert_country_name_to_code(country_name)
    nights = data_handler.calculate_number_of_nights(check_in, check_out)
    check_in = data_handler.change_dates_format(check_in)
    unique_key = search.search_post_request(search_key, country_code, geo_code, check_in, nights, rooms, stars)
    urls_hotels = search.get_the_hotels_details(unique_key)
    search.download_hotels_data(urls_hotels)


search_hotels("Berlin, Germany",

              {
                  "Latitude": "52.52000659999999",
                  "Longitude": "13.404954",
                  "PIP": "N"
              },
              "2024/03/08",
              "2024/03/9",
              [
                  {
                      "SysRoomCode": "O2A0C",
                      "NumRoom": 1,
                      "NumCots": 0,
                      "NumPax": 2,
                      "NumAdt": 2,
                      "NumCnn": 0,
                      "CnnAge1": 0,
                      "CnnAge2": 0,
                      "CnnAge3": 0,
                      "CnnAge4": 0
                  }
              ],
              3)
