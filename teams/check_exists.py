import json
import pandas as pd
from config import MATCH_PARSED_DATA_PATH, TEAMS_HASHED_LINK_PATH

ENCODING = "utf-8"

def check_exists():
    line_count = 0
    team_links_set = set()
    with open(MATCH_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
        for line in f:
            line_count += 1
            line_data = json.loads(line)
            team_links_set.add(line_data['home']['link'])
            team_links_set.add(line_data['away']['link'])

    team_links_df = pd.read_csv(TEAMS_HASHED_LINK_PATH, sep="\t")
    team_hash_links_set = set(team_links_df['url'])


    print(len(team_hash_links_set))
    print(len(team_links_set))

    check = True
    for team_link in team_hash_links_set:
        if team_link not in team_links_set:
            print(team_link)
            check = False
    if check:
        print("All team links are in the parsed data.")
    else:
        print("Some team links are not in the parsed data.")

if __name__ == "__main__":
    check_exists()
    
