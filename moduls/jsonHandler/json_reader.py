import json
import os
from os import listdir
from os.path import isfile, join


def read_json_file(filename):
    with open(filename, 'r', encoding="utf8") as f:
        json_data = json.load(f)
    return json_data


def get_json_file_names(files_folder_path):
    name_list = [item for item in listdir(files_folder_path) if isfile(join(files_folder_path, item))]
    print(name_list, files_folder_path)
    return name_list


def get_hotels_from_json(json_file):
    return json_file.get("Hotels")


def get_hotel_BPID(hotel):
    return hotel.get("Item").get("Bpid")


def remove_duplicates_hotels_ids(hotels_id_list):
    hotels_id_without_duplicates = list(set(hotels_id_list))
    return hotels_id_without_duplicates


def remove_duplicates_hotels(hotels, hotels_ids):
    hotels_without_duplicates = []
    hotel_id_without_duplicates = remove_duplicates_hotels_ids(hotels_ids)
    for hotel in hotels:
        hotel_id = get_hotel_BPID(hotel)
        if hotel_id in hotel_id_without_duplicates:
            hotels_without_duplicates.append(hotel)
            hotel_id_without_duplicates.remove(hotel_id)
    return hotels_without_duplicates


def get_all_data(files_folder_name):
    folder_name = 'files'
    files_names = get_json_file_names(files_folder_name)
    print(files_names)
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
    hotels_date, hotel_ids_list = get_all_data(folder_path)
    return remove_duplicates_hotels(hotels_date, hotel_ids_list)


def delete_jsons_files(folder_path):
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            os.remove(os.path.join(folder_path, filename))

# hotels_data = get_clean_data("files")
