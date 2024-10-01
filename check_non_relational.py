from config import *
import json

def setKeyCheck(data):
    key_check = None
    for item in data:
        keys = set(item.keys())
        if key_check is None:
            key_check = keys
        elif key_check != keys:
            return False
    return True

def typeCheck(data):
    keys = data[0].keys()
    types = {}
    for key in keys:
        types[key] = set()
    
    for item in data:
        for k,v in item.items():
            types[k].add(type(v))
    
    return types

def dataTypeCheck(data, required_types):
    for k in data.keys():
        if not data[k].issubset(required_types[k]):
            return False
    return True

def printTypeCheck(data):
    for k,v in data.items():
        print(k,'->', v)
    print('*'*20)

def check_non_relational():
    # Load the players non-relational data
    with open(PLAYERS_NON_RELATIONAL_PATH, 'r') as file:
        players_data = json.load(file)
    # Parsed player path line count
    with open(PLAYERS_PARSED_DATA_PATH, 'r') as file:
        player_line_count = sum(1 for _ in file)
    # check counts
    count_check = len(players_data) == player_line_count

    # Load the teams non-relational data
    with open(TEAMS_NON_RELATIONAL_PATH, 'r') as file:
        teams_data = json.load(file)
    # Parsed team path line count
    with open(TEAMS_PARSED_DATA_PATH, 'r') as file:
        team_line_count = sum(1 for _ in file)
    # check counts
    count_check = len(teams_data) == team_line_count and count_check

    # Load the managers non-relational data
    with open(MANAGERS_NON_RELATIONAL_PATH, 'r') as file:
        managers_data = json.load(file)
    # Parsed manager path line count
    with open(MANAGERS_PARSED_DATA_PATH, 'r') as file:
        manager_line_count = sum(1 for _ in file)
    # check counts
    count_check = len(managers_data) == manager_line_count and count_check

    # Load the players non-relational data
    with open(MATCHES_NON_RELATIONAL_PATH, 'r') as file:
        matches_data = json.load(file)
    with open(MATCH_PARSED_DATA_PATH, 'r') as file:
        match_line_count = sum(1 for _ in file)
    # check counts
    count_check = len(matches_data) == match_line_count and count_check

    if count_check:
        print('Non-relational data files are consistent with their parsed data.')
        key_check = True
        # check player keys
        if not setKeyCheck(players_data):
            print('Players data keys are inconsistent.')
            key_check = False
        # check team keys
        if not setKeyCheck(teams_data):
            print('Teams data keys are inconsistent.')
            key_check = False
        # check manager keys
        if not setKeyCheck(managers_data):
            print('Managers data keys are inconsistent.')
            key_check = False
        # check match keys
        if not setKeyCheck(matches_data):
            print('Matches data keys are inconsistent.')
            key_check = False

        if key_check:
            print('Players,Teams,Managers,Matches data keys are consistent.')
            # player types
            player_types = typeCheck(players_data)
            required_player_types = {
                'id': {str},
                'name': {str},
                'image_link': {str},
                'image_id': {str},
                'date_of_birth': {str, type(None)},
                'citizenship': {str, type(None)},
                'height': {int, type(None)},
                'position': {str, type(None)},
                'foot': {str, type(None)}
            }
            player_data_check = dataTypeCheck(player_types, required_player_types)
            if not player_data_check:
                print('Player types are inconsistent.')

            # team types
            team_types = typeCheck(teams_data)
            required_team_types = {
                'id': {str},
                'name': {str},
                'image_link': {str},
                'image_id': {str},
                'stadium': {dict, type(None)},
            }
            team_data_check = dataTypeCheck(team_types, required_team_types)
            if not team_data_check:
                print('Team types are inconsistent.')

            # manager types
            manager_types = typeCheck(managers_data)
            required_manager_types = {
                'id': {str},
                'name': {str},
                'image_link': {str},
                'image_id': {str},
                'date_of_birth': {str, type(None)},
                'citizenship': {str, type(None)},
            }
            manager_data_check = dataTypeCheck(manager_types, required_manager_types)
            if not manager_data_check:
                print('Manager types are inconsistent.')

            data_type_check = player_data_check and team_data_check and manager_data_check
            if data_type_check:
                # check ids in match
                player_ids = set([player['id'] for player in players_data])
                team_ids = set([team['id'] for team in teams_data])
                manager_ids = set([manager['id'] for manager in managers_data])

                match_ids_check = True
                for match in matches_data:
                    if match['home']['id'] not in team_ids:
                        match_ids_check = False
                        break
                    if match['away']['id'] not in team_ids:
                        match_ids_check = False
                        break
                    if match['home']['manager'] not in manager_ids:
                        match_ids_check = False
                        break
                    if match['away']['manager'] not in manager_ids:
                        match_ids_check = False
                        break
                    player_id_check = True
                    for player in match['home']['first11']:
                        if player['id'] not in player_ids:
                            player_id_check = False
                            break
                    for player in match['home']['substitutes']:
                        if player['id'] not in player_ids:
                            player_id_check = False
                            break
                    for player in match['away']['first11']:
                        if player['id'] not in player_ids:
                            player_id_check = False
                            break
                    for player in match['away']['substitutes']:
                        if player['id'] not in player_ids:
                            player_id_check = False
                            break
                    if not player_id_check:
                        match_ids_check = False
                        break
                
                
                if match_ids_check:
                    print('All ids in match data are consistent.')
                else:
                    print('Ids in match data are inconsistent.')

            else:
                print('Players,Teams,Managers data types are inconsistent.')
        
    else:
        print('Non-relational data files are inconsistent with their parsed data.')
    
if __name__ == '__main__':
    check_non_relational()
