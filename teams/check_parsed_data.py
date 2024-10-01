from config import PARSED_HTML_PATH, RAW_HTML_DIR
import os
import json

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

def checkOptionalInt(data):
    if data is None:
        return True
    if type(data) != int:
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

def checkImage(data):
    return data.startswith('https://tmssl.akamaized.net//')

# teamRec = {
#         'name': None, # string!
#         'image': None, # string!
#         'stadium': {
#             'name': None, # string?
#             'capacity': None, # int?
#         }, # string!
#     }

def check_team(team):
    error_list = []

    team_keys = ['name', 'image', 'stadium', 'id']
    if not checkRequiredObject(team, team_keys):
        error_list.append('team keys are not correct')
    else:
        if not checkRequiredString(team['name']):
            error_list.append('name is not required string')
        if not checkImage(team['image']):
            error_list.append('image is not required string')

        stadium_keys = ['name', 'capacity']
        if not checkRequiredObject(team['stadium'], stadium_keys):
            error_list.append('stadium keys are not correct')
        else:
            if not checkOptionalString(team['stadium']['name']):
                error_list.append('stadium name is not optional string')
            if not checkOptionalInt(team['stadium']['capacity']):
                error_list.append('stadium capacity is not optional int')

    return len(error_list) == 0, error_list

def print_set(data_set):
    for data in data_set:
        print(data)
        print('*'*40)
    

def check_parsed_data():
    error_ids = []
    
    name_set = set()
    image_set = set()
    stadium_name_set = set()
    stadium_capacity_set = set()

    with open(PARSED_HTML_PATH, "r", encoding=ENCODING) as f:
        lineCount = 0
        for line in f:
            try:
                data = json.loads(line.strip())
                
                name_set.add(data['name'])
                if not checkImage(data['image']):
                    image_set.add(data['image'])
                stadium_name_set.add(data['stadium']['name'])
                stadium_capacity_set.add(data['stadium']['capacity'])

                
                check, errors = check_team(data)
                lineCount += 1
                if not check:
                    print(f'Error on line {lineCount}, {errors}, -> {data['id']}')
                    error_ids.append(data['id'])
                
                
            except Exception as e:
                lineCount += 1
                print(f'Error on line {lineCount}, {e}')
                error_ids.append(data['id'])

    
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
    
