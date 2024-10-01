import os
import json
import pandas as pd
from config import MATCH_LIST_PATH, PARSED_HTML_PATH, FULL_DATA_PATH

ENCODING = "utf-8"

def check_transfermarkt_ids():
    df = pd.read_csv(MATCH_LIST_PATH, sep="\t")
    df['webId'] = df['url'].str.extract(r'/([^/]+)$')

    if df['webId'].duplicated().any():
        print("There are duplicate webIDs in the DataFrame.")
        return False
    print("No duplicate webIDs found in the DataFrame.")
    return True

def transform_date(data): # YYYY-MM-DD HH:MI
    try:
        date,time = data.split(',')[1].split(' ')
        month,day,year = date.split('/')
        
        year = f'20{year}'
        if int(month) < 10:
            month = f'0{month}'
        if int(day) < 10:
            day = f'0{day}'
        
        hour,minute = time[:-2].split(':')
        
        if time.endswith('PM'):
            if int(hour) <= 12:
                hour = f'{int(hour)+12}'
            else:
                return False
            if len(minute) != 2:
                return False
        
        elif time.endswith('AM'):
            if int(hour) < 10:
                hour = f'0{hour}'
            if len(minute) != 2:
                return False
            
        else:
            return False
        
        return f'{year}-{month}-{day} {hour}:{minute}'
            
    except Exception as e:
        return False

def transform_parsed_data():
    # Check if the match_list.txt file exists
    if not os.path.exists(MATCH_LIST_PATH):
        print("The file does not exist.")
        return False

    # Read the data from the match_list.txt file
    df = pd.read_csv(MATCH_LIST_PATH, sep="\t")
    if df.shape[0] == 0:
        print("The file is empty.")
        return False
    
    COUNTRY = "Italy"
    TYPE = "league"
    full_data = []
    with open(PARSED_HTML_PATH, "r", encoding=ENCODING) as f:
        error_count = 0 
        line_count = 0
        for line in f:
            line_count += 1
            try:
                data = json.loads(line.strip())
                date = data['date']
                if transform_date(date):
                    data['date'] = transform_date(date)

                    match = df.loc[df['id'] == data['id']].iloc[0]
                    
                    data['type'] = TYPE
                    data['league'] = match['league']
                    data['country'] = COUNTRY
                    data['season'] = match['season']
                    data['penalty'] = None
                    data['extraTime'] = None

                    full_data.append(data)
                    # print(line_count,'-',data['id'],'-',match['league'],'-',match['season'],'-',data['date'])
                else:
                    print(f'Error on line {line_count}, Invalid date format.')
                    error_count += 1

                
            except Exception as e:
                print(f'Error on line {line_count}, {e},{type(e)}')

    # Load the parsed pages
    parsed_id_list = []
    if os.path.exists(FULL_DATA_PATH):
        with open(FULL_DATA_PATH, "r", encoding=ENCODING) as f:
            # Saving the parsed ids to avoid reparsing them
            for line in f:
                data = json.loads(line.strip())
                id_str = data["id"]
                parsed_id_list.append(id_str)
    else:
        with open(FULL_DATA_PATH, "w", encoding=ENCODING) as f:
            pass
    
    errorIds = []
    for match_data in full_data:
        # Skip if already parsed
        if match_data['id'] in parsed_id_list:
            continue
        else:
            try:
                # Saving the parsed data
                with open(FULL_DATA_PATH, "a", encoding=ENCODING) as f:
                    f.write("{}\n".format(json.dumps(match_data)))
            except Exception as e:
                print(f"Failed to parse data {match_data['id']}: {e}")
                errorIds.append(match_data['id'])

    print("ERROR Ids")
    for e in errorIds:
        print(e)
        print('-----------------')
        
if __name__ == "__main__":
    is_unique = check_transfermarkt_ids()
    if is_unique:
        transform_parsed_data()