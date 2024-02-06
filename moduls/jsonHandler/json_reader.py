import json
import os
from os import listdir
from os.path import isfile, join


def read_json_file(filename):
    """
    Reads the json
    :param filename: the name of the json file to read
    :return: the data in the json file
    """
    with open(filename, 'r', encoding="utf8") as f:
        json_data = json.load(f)
    return json_data


def get_json_file_names(files_folder_path):
    """
    Over on files dictionary and returns a list of filenames
    :param files_folder_path: the path of the json files dictionary
    :return: list of filenames
    """
    name_list = [item for item in listdir(files_folder_path) if isfile(join(files_folder_path, item))]
    return name_list


def get_hotels_from_json(json_file):
    """
    Reads the json file and returns a list of hotels
    :param json_file: the name of the json file to read
    :return: a list of hotels
    """
    return json_file.get("Hotels")


def get_hotel_BPID(hotel):
    """
    Reads the hotel and its BPID
    :param hotel: the hotel to read
    :return:the BPID of the hotel
    """
    return hotel.get("Item").get("Bpid")


def remove_duplicates_hotels_ids(hotels_id_list):
    """
    Removes duplicate hotels ids from a list of hotels ids
    :param hotels_id_list: the list of hotels ids
    :return: the list of hotels ids without duplicates
    """
    hotels_id_without_duplicates = list(set(hotels_id_list))
    return hotels_id_without_duplicates


def remove_duplicates_hotels(hotels, hotels_ids):
    """
    Removes duplicate hotels from hotels list according to their ids
    :param hotels: the list of hotels
    :param hotels_ids: the list of hotels ids without duplicates
    :return: the list of hotels without duplicates
    """
    hotels_without_duplicates = []
    hotel_id_without_duplicates = remove_duplicates_hotels_ids(hotels_ids)
    for hotel in hotels:
        hotel_id = get_hotel_BPID(hotel)
        if hotel_id in hotel_id_without_duplicates:
            hotels_without_duplicates.append(hotel)
            hotel_id_without_duplicates.remove(hotel_id)
    return hotels_without_duplicates


def get_all_data(files_folder_name):
    """
    get the data from the json files
    :param files_folder_name:the name folder of the json files
    :return:the hotel and hotel ids
    """
    folder_name = 'files'
    files_names = get_json_file_names(files_folder_name)
    hotel_data_list = []
    hotel_ids_list = []
    for name in files_names:
        json_data = read_json_file(f'{folder_name}/{name}')
        hotels = get_hotels_from_json(json_data)
        for hotel in hotels:
            hotel_data_list.append(hotel)
            hotel_ids_list.append(get_hotel_BPID(hotel))
    return hotel_data_list, hotel_ids_list


def get_clean_data(folder_path):
    """
    get the data from the json files without duplicates
    :param folder_path: the folder path of the json files
    :return: the data without duplicates
    """
    hotels_date, hotel_ids_list = get_all_data(folder_path)
    return remove_duplicates_hotels(hotels_date, hotel_ids_list)


def delete_jsons_files(folder_path):
    """
    delete the json files from folder
    :param folder_path: the folder path to delete the json files
    :return: None
    """
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            os.remove(os.path.join(folder_path, filename))


