import os



def delete_json_file(files_name_list):
    for file_name in files_name_list:
        if os.path.isfile(file_name):
            os.remove(file_name)

