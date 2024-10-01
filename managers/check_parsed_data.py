from config import PARSED_HTML_PATH, RAW_HTML_DIR
import os
import json
from datetime import datetime

ENCODING = "utf-8"

def checkRequiredString(data):
    if data is None:
        return False
    if type(data) != str:
        return False
    if len(data) == 0:
        return False
    return True

def checkOptionalString(data):
    if data is None:
        return True
    if type(data) != str:
        return False
    if len(data) == 0:
        return False
    return True

def checkRequiredObject(data, keys):
    if data is None:
        return False
    if type(data) != dict:
        return False
    if set(data.keys()) != set(keys):
        return False
    return True

def checkDateOfBirth(data):
    if data is None:
        return True
    try:
        # Attempt to parse the date string with the expected format
        datetime.strptime(data, "%b %d, %Y")
        return True
    except ValueError:
        # If a ValueError is raised, the format is incorrect
        return False
    
def checkImage(data):
    return data.startswith('https://img.a.transfermarkt.technology/portrait/header')

# managerRec = {
#         'name': None, #string!
#         'image': None, #string!
#         'date_of_birth': None, #string?
#         'citizenship': None, #string?
#     }

def check_manager(manager):
    error_list = []

    manager_keys = ['name', 'image', 'date_of_birth', 'citizenship','id']
    if not checkRequiredObject(manager, manager_keys):
        error_list.append('manager keys are not correct')
    else:
        if not checkRequiredString(manager['name']):
            error_list.append('name is not required string')
        if not checkImage(manager['image']):
            error_list.append('image is not required string')
        if not checkDateOfBirth(manager['date_of_birth']):
            error_list.append('date of birth is not optional string')
        if not checkOptionalString(manager['citizenship']):
            error_list.append('citizenship is not optional int')

    return len(error_list) == 0, error_list

def print_set(data_set):
    for data in data_set:
        print(data)
        print('*'*40)
    

def check_parsed_data():
    error_ids = []

    name_set = set()
    image_set = set()
    date_of_birth_set = set()
    citizenship_set = set()

    with open(PARSED_HTML_PATH, "r", encoding=ENCODING) as f:
        lineCount = 0
        for line in f:
            try:
                data = json.loads(line.strip())
                
                name_set.add(data['name'])
                image_set.add(data['image'])
                if not checkDateOfBirth(data['date_of_birth']):
                    date_of_birth_set.add(data['date_of_birth'])
                citizenship_set.add(data['citizenship'])

                check, errors = check_manager(data)
                lineCount += 1
                if not check:
                    print(f'Error on line {lineCount}, {errors}, -> {data['id']}')
                    error_ids.append(data['id'])
                
                
            except Exception as e:
                lineCount += 1
                print(f'Error on line {lineCount}, {e}')
                error_ids.append(data['id'])

    # print_set(name_set)
    # print_set(image_set)
    # print_set(date_of_birth_set) 
    # print_set(citizenship_set) 

    
    # ### REMOVE ERROR FILES
    # # Specify the path to the file
    # for error_id in error_ids:
    #     try:
    #         file_path = os.path.join(RAW_HTML_DIR, error_id + '.html')
    #         # Check if the file exists
    #         if os.path.exists(file_path):
    #             os.remove(file_path)
    #             print(f"{error_id}.html removed successfully")
    #         else:
    #             print(f"{error_id}.html does not exist")

    #         print('*'*40)
    #     except Exception as e:
    #         print(f"Failed to remove {error_id}.html: {e}")
    #         print('*'*40)


if __name__ == "__main__":
    print(len(os.listdir(RAW_HTML_DIR)))
    check_parsed_data()
    
