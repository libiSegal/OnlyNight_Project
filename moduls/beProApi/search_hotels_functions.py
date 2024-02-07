import gzip
import json
import time
import base64
import requests
import xml.etree.ElementTree as ET
from datetime import date
from io import BytesIO
from moduls.jsonHandler import json_reader as jdr
from moduls.beProApi import bepro_definitions as definition
from moduls.beProApi import hotels_data_handler as hotel_handler

last_index = './/ItemsLinkAsyncResults'


def search_post_request(search_key, country_code, geo_code, check_in, nights, rooms, stars, radius):
    """
    This function will send a post request to bepro api and search for hotels by all parameters
    :param radius: the radius of distance to search
    :param search_key: the city and country to search
    :param country_code: the country code
    :param geo_code: the geographic code for the city
    :param check_in: the date to begin searching
    :param nights: the number of nights to search
    :param rooms: the details of the room to search
    :param stars: the number of the hotels starts
    :return: the unique key of the response
    """
    # all the data here is from bepro documentation
    post_search_url = "https://pub_srv.beprotravel.net/BePro/api/Hotels/SearchQuery"
    payload = json.dumps({
        "Query": {
            "SearchResponceType": 7,
            "SearchType": 0,
            "GeoSearch": {
                "Radius": radius,
                "HavePIP": False,
                "SearchKey": {
                    "Name": search_key
                },
                "CountryCode": {
                    "Code": country_code
                },
                "GeoCode": geo_code,
                "SearchGeoType": 2,
                "AltSeacrhKey": None
            },
            "CheckIn": check_in,
            "Nights": nights,
            "Rooms": rooms,
            "StarRateCode": stars,
            "CurrencyCode": "USD",
            "RetFilterFromResults": True,
            "RemoveSmallRooms": True,
            "ClientType": "B2C",
            "SearchTypeId": 138,
            "Command": 0,
            "LanguageCode": "en",
            "CompanyId": definition.company_id,
            "DepartmentId": definition.department_id,
            "BranchId": definition.branc_id,
            "UserCode": definition.user_code,
            "MaxMilliSecondsTimeToWait": definition.max_milli_seconds_time_to_wait
        },
        "Header": {
            "CompanyId": definition.company_id,
            "DepartmentId": definition.department_id,
            "BranchId": definition.branc_id,
            "UserCode": definition.user_code,
            "UserId": definition.user_id,
            "UserPWD": definition.user_pwd
        }
    })
    headers = {
        'Accept': 'application/json',
        'BEPROCOMPANY': '135',
        'Content-Type': 'application/json',
        'Authorization': 'Basic Qz0xMzU6RD0xOkI9MjAwOlU9MjI1MDpQPTE5RDdC'
    }
    response = requests.request("POST", post_search_url, headers=headers, data=payload, verify=False)
    return get_the_unique_key(response.json())


def get_the_hotels_details(unique_key):
    """
    Send request to get details of all hotels till all data return
    :param unique_key: the unique key of the post request to get the details of hotels
    :return: a list of urls with the details of all hotels
    """
    status = "CompleteMayBeDisposed"
    multi_key = 'Not finish, but empty'
    response = get_hotels_request(unique_key)
    res_multi_key = get_response_multiKey(response)
    res_status = get_response_status(response)
    urls = get_hotels_urls(response)
    while res_status != status and res_multi_key != multi_key:
        response = get_hotels_request(unique_key)
        multi_key = get_response_multiKey(response)
        status = get_response_status(response)
        urls += get_hotels_urls(response)
    return urls


def get_hotels_request(unique_key):
    """
    Send a get request by unique key to the bepro api and return a xml with urls of hotels
    :param unique_key: the unique key to get from the bepro api the data
    :return: the response
    """
    # all the data here is from bepro documentation
    get_hotels_details_url = (f"https://pub_srv.beprotravel.net/BePro/api/Hotels/GetJsonResults?"
                              f"token={unique_key}&compress=false")
    headers = {
        'BEPROCOMPANY': '135',
        'Authorization': 'Basic Qz0xMzU6RD0xOkI9MjAwOlU9MjI1MDpQPTE5RDdC'
    }
    time_sleep = 6
    time.sleep(time_sleep)
    response = requests.request("GET", get_hotels_details_url, headers=headers, verify=False)
    return response.text


def get_response_multiKey(xml_response):
    """
    return the multi key of the xml response
    :param xml_response: a xml response that return from the bepro api
    :return: the multi key of the xml response
    """
    root = ET.fromstring(xml_response)
    multi_key = [item.find('MultiKey').text for item in root.findall(last_index)]
    return multi_key[0]


def get_response_status(xml_response):
    """
    return the status of the xml response
    :param xml_response: a xml response that return from the bepro api
    :return: the status of the xml response
    """
    root = ET.fromstring(xml_response)
    status = [item.find('Status').text for item in root.findall(last_index)]
    return status[0]


def get_hotels_urls(xml_response):
    """
    except from the response only the url fields
    :param xml_response: the xml response
    :return: a list of urls
    """
    root = ET.fromstring(xml_response)
    urls = [item.find('Url').text for item in root.findall('ItemsLinkAsyncResults')]
    return urls


def get_the_unique_key(json_response):
    """
    extract the unique key of the response
    :param json_response: the searching response from the api
    :return: the unique key field
    """
    return json_response.get('results').get('sysResinfo').get('uniqueKey')


def decompress(compressed_file):
    """
    decompress the file that return from the bepro api request
    :param compressed_file: the file to decompress
    :return: the decompressed file
    """
    try:
        if compressed_file is None or len(compressed_file) == 0:
            return None
        if "<?xml version" in compressed_file:
            return compressed_file

        g_zip_buffer = base64.urlsafe_b64decode(compressed_file)

        with BytesIO() as memory_stream:
            data_length = int.from_bytes(g_zip_buffer[:4], byteorder='little')
            memory_stream.write(g_zip_buffer[4:])

            buffer = bytearray(data_length)
            memory_stream.seek(0)

            with gzip.GzipFile(fileobj=memory_stream, mode='rb') as g_zip_stream:
                total_read = 0
                while total_read < data_length:
                    bytes_read = g_zip_stream.readinto(buffer)
                    if bytes_read == 0:
                        break
                    total_read += bytes_read

                return buffer.decode('utf-8').rstrip('\x00')
    except:
        return None


def download_hotels_data(url_list):
    """
    Download the files from the url list and save them in jsons files
    :param url_list: a list of the urls to download
    :return: None
    """
    if url_list[0] is None:
        return "No hotels found"
    for i in range(len(url_list)):
        if url_list[i] is not None:
            response = requests.get(url_list[i], verify=False)
            compressed_file = response.text
            decompressed_file = decompress(compressed_file)
            if decompressed_file is not None:
                name = get_name_from_url(url_list[i])
                output_path = "files"
                output_path = f"{output_path}/{name}.json"
                save_hotels_data(decompressed_file, output_path)


def save_hotels_data(data, output_path):
    """
    Save hotels data to json file
    :param data: the hotels data to be saved
    :param output_path: the path to save the json file
    :return: None
    """
    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(data)


def get_name_from_url(url):
    """
    Get name from each file to download
    :param url: to take the name from
    :return: the name of the file
    """
    name = url.split('/')[-1]
    name = name.replace('.zip', "_" + str(date.today()))
    return name


def insert_hotels_data_into_db():
    """
    the function take the hotels from the files directory and insert them into the database
    :return: None
    """
    hotels = jdr.get_clean_data(r'files')
    if hotels is not None:
        for hotel in hotels:
            return hotel_handler.handle_data_hotel(hotel)
