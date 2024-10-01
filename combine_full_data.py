import os
import json
from config import MATCH_PARSED_DATA_PATH

def combine_full_data():
    root = 'transfermarkt'
    league_folders = os.listdir(root)
    ENCODING = 'utf-8'

    data = []
    for league_folder in league_folders:
        data_path = os.path.join(root, league_folder, 'data', 'full_data.jsons')
        # check if the file exists
        if os.path.exists(data_path):
            print(f"Reading data from {data_path}")
            with open(data_path, "r", encoding=ENCODING) as f:
                for line in f:
                    data.append(json.loads(line.strip()))
        else:
            print(f"File does not exist: {data_path}")
        print('-----------------')


    print("Reading parsed data")
    
    parsedIds = []
    # Check if the file exists
    if os.path.exists(MATCH_PARSED_DATA_PATH):
        with open(MATCH_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
            for line in f:
                line_data = (json.loads(line.strip()))
                id_str = line_data["id"]
                parsedIds.append(id_str)
    else:
        with open(MATCH_PARSED_DATA_PATH, "w", encoding=ENCODING) as f:
            pass

    print("Combining data")
    errorIds = []
    for match_data in data:
        if match_data['id'] in parsedIds:
            continue
        try:
            # Saving the parsed data
            with open(MATCH_PARSED_DATA_PATH, "a", encoding=ENCODING) as f:
                f.write("{}\n".format(json.dumps(match_data)))
        except Exception as e:
            print(f"Failed to parse data {match_data['id']}: {e}")
            errorIds.append(match_data['id'])
    
    if len(errorIds) > 0:
        print("ERROR Ids")
        for e in errorIds:
            print(e)
            print('-----------------')

if __name__ == "__main__":
    # combine_full_data()
    ids = []
    keys = None
    check = True
    with open(MATCH_PARSED_DATA_PATH, "r", encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            if keys is None:
                keys = data.keys()
            elif set(keys) != set(data.keys()):
                print('Keys are not the same')
                check = False
            ids.append(data['id'])
    
    print(f"Number of ids: {len(ids)}")
    print(f"Number of unique ids: {len(set(ids))}")
    print(f"Check: {check}")
    print(f"Keys: {keys}")
            
        