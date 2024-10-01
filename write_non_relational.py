from config import *
import json
from datetime import datetime
import pandas as pd
import os

def formatDate(data):
    if data is None:
        return None
    try:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(data, "%b %d, %Y")
        # Format the datetime object into the desired string format
        formatted_date = date_obj.strftime("%Y-%m-%d")

        return formatted_date
    except:
        return None
def formatStadium(data):
    if data['name'] is None and data['capacity'] is None:
        return None
    return data

def attachManager(data,managers_df):
    manager_keys = set(['name','link'])
    if set(data.keys()) != manager_keys:
        return None
    try:
        manager_id = managers_df.loc[managers_df['link'] == data['link'], 'id'].iloc[0]
        return manager_id
    except:
        return None
def attachPlayer(data,players_df):
    player_keys = set(['number', 'name', 'link', 'position', 'actions'])
    if set(data.keys()) != player_keys:
        return None
    try:
        player_id = players_df.loc[players_df['link'] == data['link'], 'id'].iloc[0]
        return {
            'id': player_id,
            'number': data['number'],
            'position': data['position'],
            'actions': data['actions']
        }
    except:
        return None
def attachTeam(data,teams_df):
    team_keys = set(['name', 'link', 'position', 'score', 'halfScore', 'first11', 'substitutes', 'lineup', 'manager'])
    if set(data.keys()) != team_keys:
        return None
    try:
        team_id = teams_df.loc[teams_df['url'] == data['link'], 'teamId'].iloc[0]
        return {
            'id': team_id,
            'position': data['position'],
            'score': data['score'],
            'halfScore': data['halfScore'],
            'first11': data['first11'],
            'substitutes': data['substitutes'],
            'lineup': data['lineup'],
            'manager': data['manager']
        }
    except:
        return None
def attachMatch(data,managers_df,players_df,teams_df):
    match_keys = set(['home', 'away', 'extraTime', 'penalty', 'round', 'date', 'stadium', 'attendance', 'referee', 'id', 'type', 'league', 'country', 'season'])
    
    if set(data.keys()) != match_keys:
        print('Incorrect match keys')
        return None
    
    # attach home manager
    home_manager = attachManager(data['home']['manager'],managers_df)
    if home_manager is None:
        print(f"Home Manager not found: {data['id']}")
        return None
    data['home']['manager'] = home_manager
    
    # attach away manager
    away_manager = attachManager(data['away']['manager'],managers_df)
    if away_manager is None:
        print(f"Away Manager not found: {data['id']}")
        return None
    data['away']['manager'] = away_manager

    # attach home first11
    home_first11 = []
    for player in data['home']['first11']:
        attached_player = attachPlayer(player,players_df)
        if attached_player is None:
            print(f"Home Player not found: {data['id']}")
            return None
        home_first11.append(attached_player)
    data['home']['first11'] = home_first11

    # attach away first11
    away_first11 = []
    for player in data['away']['first11']:
        attached_player = attachPlayer(player,players_df)
        if attached_player is None:
            print(f"Away Player not found: {data['id']}")
            return None
        away_first11.append(attached_player)
    data['away']['first11'] = away_first11

    # attach home substitutes
    home_substitutes = []
    for player in data['home']['substitutes']:
        attached_player = attachPlayer(player,players_df)
        if attached_player is None:
            print(f"Home Substitute Player not found: {data['id']}")
            return None
        home_substitutes.append(attached_player)
    data['home']['substitutes'] = home_substitutes

    # attach away substitutes
    away_substitutes = []
    for player in data['away']['substitutes']:
        attached_player = attachPlayer(player,players_df)
        if attached_player is None:
            print(f"Away Substitute Player not found: {data['id']}")
            return None
        away_substitutes.append(attached_player)
    data['away']['substitutes'] = away_substitutes

    # attach home team
    home_team = attachTeam(data['home'],teams_df)
    if home_team is None:
        print(f"Home Team not found: {data['id']}")
        return None
    data['home'] = home_team

    # attach away team
    away_team = attachTeam(data['away'],teams_df)
    if away_team is None:
        print(f"Away Team not found: {data['id']}")
        return None
    data['away'] = away_team

    return {
        'id': data['id'],
        'type': data['type'],
        'league': data['league'],
        'country': data['country'],
        'season': data['season'],
        'round': data['round'],
        'date': data['date'],
        'stadium': data['stadium'],
        'attendance': data['attendance'],
        'referee': data['referee'],
        'extraTime': data['extraTime'],
        'penalty': data['penalty'],
        'home': data['home'],
        'away': data['away']
    }

    
ENCODING = "utf-8"
images_df = pd.read_csv(IMAGE_LINKS_PATH, sep="\t")

def write_manager():
    if os.path.exists(MANAGERS_NON_RELATIONAL_PATH):
        print(f"File already exists: {MANAGERS_NON_RELATIONAL_PATH}") 
    else:
        manager_ids = set()
        check = True
        data = []

        with open(MANAGERS_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
            for line in f:
                line_data = (json.loads(line.strip()))
                id_str = line_data["id"]
                if id_str in manager_ids:
                    check = False
                    print("Duplicate ID found")
                    break
                else:
                    manager_ids.add(id_str)
                
                try:
                    image_id = images_df.loc[images_df['url'] == line_data['image'], 'id'].iloc[0]
                except:
                    check = False
                    print("Image id not found")
                    break

                formatted_data = {
                    'id': line_data['id'],
                    'name': line_data['name'],
                    'image_link': line_data['image'],
                    'image_id': image_id,
                    'date_of_birth': formatDate(line_data['date_of_birth']),
                    'citizenship': line_data['citizenship']
                }
                data.append(formatted_data)

        if check:
            with open(MANAGERS_NON_RELATIONAL_PATH, 'w', encoding='utf-8') as managers_file:
                json.dump(data, managers_file, ensure_ascii=False, indent=4)

def write_team():
    if os.path.exists(TEAMS_NON_RELATIONAL_PATH):
        print(f"File already exists: {TEAMS_NON_RELATIONAL_PATH}") 
    else:
        team_ids = set()
        check = True
        data = []

        with open(TEAMS_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
            for line in f:
                line_data = (json.loads(line.strip()))
                id_str = line_data["id"]
                if id_str in team_ids:
                    check = False
                    print("Duplicate ID found")
                    break
                else:
                    team_ids.add(id_str)
                
                try:
                    image_id = images_df.loc[images_df['url'] == line_data['image'], 'id'].iloc[0]
                except:
                    check = False
                    print("Image id not found")
                    break

                formatted_data = {
                    'id': line_data['id'],
                    'name': line_data['name'],
                    'image_link': line_data['image'],
                    'image_id': image_id,
                    'stadium': formatStadium(line_data['stadium']),
                }
                data.append(formatted_data)

        if check:
            with open(TEAMS_NON_RELATIONAL_PATH, 'w', encoding='utf-8') as teams_file:
                json.dump(data, teams_file, ensure_ascii=False, indent=4)

def write_player():
    if os.path.exists(PLAYERS_NON_RELATIONAL_PATH):
        print(f"File already exists: {PLAYERS_NON_RELATIONAL_PATH}") 
    else:
        player_ids = set()
        check = True
        data = []

        with open(PLAYERS_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
            for line in f:
                line_data = (json.loads(line.strip()))
                id_str = line_data["id"]
                if id_str in player_ids:
                    check = False
                    print("Duplicate ID found")
                    break
                else:
                    player_ids.add(id_str)
                
                try:
                    image_id = images_df.loc[images_df['url'] == line_data['image'], 'id'].iloc[0]
                except:
                    check = False
                    print("Image id not found")
                    break
            
                formatted_data = {
                    'id': line_data['id'],
                    'name': line_data['name'],
                    'image_link': line_data['image'],
                    'image_id': image_id,
                    'date_of_birth': formatDate(line_data['date_of_birth']),
                    'citizenship': line_data['citizenship'],
                    'height': line_data['height'],
                    'position': line_data['position'],
                    'foot': line_data['foot'],
                }
                data.append(formatted_data)

        if check:
            with open(PLAYERS_NON_RELATIONAL_PATH, 'w', encoding='utf-8') as teams_file:
                json.dump(data, teams_file, ensure_ascii=False, indent=4)

def write_match():
    if not os.path.exists(MANAGERS_NON_RELATIONAL_PATH) or not os.path.exists(TEAMS_NON_RELATIONAL_PATH) or not os.path.exists(PLAYERS_NON_RELATIONAL_PATH):
        print(f"{MANAGERS_NON_RELATIONAL_PATH}, {TEAMS_NON_RELATIONAL_PATH}, {PLAYERS_NON_RELATIONAL_PATH} does not exist")
    elif os.path.exists(MATCHES_NON_RELATIONAL_PATH):
        print(f"File already exists: {MATCHES_NON_RELATIONAL_PATH}") 
    else:
        match_ids = set()
        check = True
        data = []

        count = 0
        with open(MATCH_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
            for line in f:
                line_data = (json.loads(line.strip()))
                id_str = line_data["id"]
                if id_str in match_ids:
                    check = False
                    print("Duplicate ID found")
                    break
                else:
                    match_ids.add(id_str)
        
                    # construct managers DF
                    managers_df = pd.read_csv(MANAGERS_HASH_LIST_PATH, sep="\t")
                    # construct teams DF
                    teams_df = pd.read_csv(TEAMS_HASH_LIST_PATH, sep="\t")
                    # construct players DF
                    players_df = pd.read_csv(PLAYERS_HASH_LIST_PATH, sep="\t")

                    # attach match
                    match = attachMatch(line_data,managers_df,players_df,teams_df)
                    if match is None:
                        check = False
                        break
                    else:
                        count += 1
                        print(f"Match {count}/9202")
                        data.append(match)

        if check:
            with open(MATCHES_NON_RELATIONAL_PATH, 'w', encoding='utf-8') as teams_file:
                json.dump(data, teams_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # write_manager()
    # write_team()
    # write_player()
    write_match()