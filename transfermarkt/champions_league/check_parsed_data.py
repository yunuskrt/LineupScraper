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

def checkRequiredInt(data):
    if data is None:
        return False
    if type(data) != int:
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

def checkRequiredList(data):
    if data is None:
        return False
    if type(data) != list:
        return False
    return True

def checkNone(data):
    return data is None

def check_match(match):
    error_list = []

    match_keys = ['home', 'away', 'round', 'date', 'stadium','attendance', 'referee', 'id', 'penalty', 'extraTime']
    if not checkRequiredObject(match, match_keys):
        error_list.append('match keys are not correct')
    else:
        home_keys = ['name', 'link', 'position', 'score', 'halfScore', 'first11', 'substitutes', 'lineup', 'manager']
        home = match['home']
        if not checkRequiredObject(home, home_keys):
            error_list.append('home keys are not correct')
        else:
            if not checkRequiredString(home['name']):
                error_list.append('home name is not required string')
            if not checkRequiredString(home['link']):
                error_list.append('home link is not required string')
            if not checkNone(home['position']):
                error_list.append('home position is not none')
            if not checkRequiredInt(home['score']):
                error_list.append('home score is not required int')
            if not checkOptionalInt(home['halfScore']):
                error_list.append('home halfScore is not optional int')
            if not checkRequiredList(home['first11']):
                error_list.append('home first11 is not required list')
            elif len(home['first11']) != 11:
                error_list.append('home first11 length is not 11')
            else:
                for player in home['first11']:
                    player_keys = ['number', 'name', 'link', 'position', 'actions']
                    if not checkRequiredObject(player, player_keys):
                        error_list.append('home player keys are not correct')
                    else:
                        if not checkOptionalInt(player['number']):
                            error_list.append('home player number is not optional int')
                            break
                        if not checkRequiredString(player['name']):
                            error_list.append('home player name is not required string')
                            break
                        if not checkRequiredString(player['link']):
                            error_list.append('home player link is not required string')
                            break
                        if not checkRequiredString(player['position']):
                            error_list.append('home player position is not required string')
                            break
                        if not checkRequiredList(player['actions']):
                            error_list.append('home player actions is not required list')
                            break
            
            if not checkRequiredList(home['substitutes']):
                error_list.append('home substitutes is not required list')
            else:
                for player in home['substitutes']:
                    player_keys = ['number', 'name', 'link', 'position', 'actions']
                    if not checkRequiredObject(player, player_keys):
                        error_list.append('home player keys are not correct')
                    else:
                        if not checkOptionalInt(player['number']):
                            error_list.append('home substitute player number is not optional int')
                            break
                        if not checkRequiredString(player['name']):
                            error_list.append('home substitute player name is not required string')
                            break
                        if not checkRequiredString(player['link']):
                            error_list.append('home substitute player link is not required string')
                            break
                        if not checkOptionalString(player['position']):
                            error_list.append('home substitute player position is not optional string')
                            break
                        if not checkRequiredList(player['actions']):
                            error_list.append('home substitute player actions is not required list')
                            break
            if not checkRequiredString(home['lineup']):
                error_list.append('home lineup is not required string')
            if not checkRequiredObject(home['manager'], ['name', 'link']):
                error_list.append('home manager keys are not correct')
            else:
                manager = home['manager']
                if not checkRequiredString(manager['name']):
                    error_list.append('home manager name is not required string')
                if not checkRequiredString(manager['link']):
                    error_list.append('home manager link is not required string')
    
        away_keys = ['name', 'link', 'position', 'score', 'halfScore', 'first11', 'substitutes', 'lineup', 'manager']
        away = match['away']
        if not checkRequiredObject(away, away_keys):
            error_list.append('away keys are not correct')
        else:
            if not checkRequiredString(away['name']):
                error_list.append('away name is not required string')
            if not checkRequiredString(away['link']):
                error_list.append('away link is not required string')
            if not checkNone(away['position']):
                error_list.append('away position is not none')
            if not checkRequiredInt(away['score']):
                error_list.append('away score is not required int')
            if not checkOptionalInt(away['halfScore']):
                error_list.append('away halfScore is not optional int')
            if not checkRequiredList(away['first11']):
                error_list.append('away first11 is not required list')
            elif len(away['first11']) != 11:
                error_list.append('away first11 length is not 11')
            else:
                for player in away['first11']:
                    player_keys = ['number', 'name', 'link', 'position', 'actions']
                    if not checkRequiredObject(player, player_keys):
                        error_list.append('away player keys are not correct')
                    else:
                        if not checkOptionalInt(player['number']):
                            error_list.append('away player number is not optional int')
                            break
                        if not checkRequiredString(player['name']):
                            error_list.append('away player name is not required string')
                            break
                        if not checkRequiredString(player['link']):
                            error_list.append('away player link is not required string')
                            break
                        if not checkRequiredString(player['position']):
                            error_list.append('away player position is not required string')
                            break
                        if not checkRequiredList(player['actions']):
                            error_list.append('away player actions is not required list')
                            break
            
            if not checkRequiredList(away['substitutes']):
                error_list.append('away substitutes is not required list')
            else:
                for player in away['substitutes']:
                    player_keys = ['number', 'name', 'link', 'position', 'actions']
                    if not checkRequiredObject(player, player_keys):
                        error_list.append('away player keys are not correct')
                    else:
                        if not checkOptionalInt(player['number']):
                            error_list.append('away substitute player number is not optional int')
                        if not checkRequiredString(player['name']):
                            error_list.append('away substitute player name is not required string')
                        if not checkRequiredString(player['link']):
                            error_list.append('away substitute player link is not required string')
                        if not checkOptionalString(player['position']):
                            error_list.append('away substitute player position is not optional string')
                        if not checkRequiredList(player['actions']):
                            error_list.append('away substitute player actions is not required list')

            if not checkRequiredString(away['lineup']):
                error_list.append('away lineup is not required string')
            
            if not checkRequiredObject(away['manager'], ['name', 'link']):
                error_list.append('away manager keys are not correct')
            else:
                manager = away['manager']
                if not checkRequiredString(manager['name']):
                    error_list.append('away manager name is not required string')
                if not checkRequiredString(manager['link']):
                    error_list.append('away manager link is not required string')

    if not checkRequiredString(match['round']):
        error_list.append('round is not required string')
    if not checkRequiredString(match['date']):
        error_list.append('date is not required string')
    if not checkOptionalString(match['stadium']):
        error_list.append('stadium is not required string')
    if not checkOptionalInt(match['attendance']):
        error_list.append('attendance is not optional int')
    if not checkRequiredString(match['referee']):
        error_list.append('referee is not required string')
    if not checkRequiredString(match['id']):
        error_list.append('id is not required string')

    return len(error_list) == 0, error_list

def check_parsed_data():
    error_ids = []
    with open(PARSED_HTML_PATH, "r", encoding=ENCODING) as f:
        lineCount = 0
        for line in f:
            try:
                data = json.loads(line.strip())
                check, errors = check_match(data)
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
    
