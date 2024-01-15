import json
from os import listdir
from os.path import isfile, join


def read_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def get_json_file_names(folder_path):
    return [item for item in listdir(folder_path) if isfile(join(folder_path, item))]




