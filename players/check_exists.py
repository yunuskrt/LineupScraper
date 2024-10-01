import json
import pandas as pd

from config import MATCH_PARSED_DATA_PATH, PLAYERS_LINK_PATH

ENCODING = "utf-8"

def check_exists():
    line_count = 0
    player_match_links_set = set()
    with open(MATCH_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
        for line in f:
            line_count += 1
            line_data = json.loads(line)
            homeFirst11, homeSubs = line_data['home']['first11'], line_data['home']['substitutes']
            awayFirst11, awaySubs = line_data['away']['first11'], line_data['away']['substitutes']
            for player in homeFirst11:
                player_match_links_set.add(player['link'])
            for player in homeSubs:
                player_match_links_set.add(player['link'])
            for player in awayFirst11:
                player_match_links_set.add(player['link'])
            for player in awaySubs:
                player_match_links_set.add(player['link'])

    
    player_links_df = pd.read_csv(PLAYERS_LINK_PATH, sep="\t")
    player_links_set = set(player_links_df['link'])


    print(len(player_match_links_set))
    print(len(player_links_set))

    check = True
    for player_link in player_links_set:
        if player_link not in player_match_links_set:
            print(player_link)
            check = False

    if check:
        print("All player links are in the parsed data.")
    else:
        print("Some player links are not in the parsed data.")

if __name__ == "__main__":
    check_exists()
    
