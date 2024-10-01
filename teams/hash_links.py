import os
import pandas as pd

from config import TEAMS_SEASONS_LINK_PATH, TEAMS_LINK_PATH, TEAMS_HASHED_LINK_PATH

ENCODING = "utf-8"

def save_hashed_link(id, link, team_id):
    with open(TEAMS_HASHED_LINK_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id, link, team_id]) + "\n")
    pass

def hash_links():
    if not os.path.exists(TEAMS_HASHED_LINK_PATH):
        with open(TEAMS_HASHED_LINK_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "teamId"]) + "\n")
    
    print("Hashing links")
    
    df_team_links = pd.read_csv(TEAMS_LINK_PATH, sep="\t")
    teamLinks = {}
    for idx, row in df_team_links.iterrows():
        if row["link"] in teamLinks:
            print("Duplicate link found: ", row["link"])
        else:
            teamLinks[row["link"]] = row["id"]
    
    check = True
    teamIds = {}
    df_team_seasons = pd.read_csv(TEAMS_SEASONS_LINK_PATH, sep="\t")
    for idx, row in df_team_seasons.iterrows():
        team_url = '/'.join(row['url'].split('/')[:5])
        if team_url in teamLinks:
            team_id = teamLinks[team_url]
            teamIds[row['id']] = team_id
        else:
            check = False
            print(idx, '->',team_url,' not found')
    
    if check:
        for idx, row in df_team_seasons.iterrows():
            id,url,teamId = row['id'],row['url'],teamIds[row['id']]
            save_hashed_link(id, url, teamId)
        print('All links found')    
        
if __name__ == "__main__":
    hash_links()
    
