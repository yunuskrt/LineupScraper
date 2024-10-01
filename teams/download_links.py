import os
import pandas as pd
import uuid
from config import TEAMS_SEASONS_LINK_PATH, TEAMS_LINK_PATH

ENCODING = "utf-8"


def save_link(link):
    # Save collected link/url and page to the .txt file in MATCH_LIST_PATH
 
    baseUrl = "https://www.transfermarkt.com"
    url = baseUrl + link
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(TEAMS_LINK_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, link, url]) + "\n")

def download_links_from_index():
    if not os.path.exists(TEAMS_LINK_PATH):
        with open(TEAMS_LINK_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "link", "url"]) + "\n")

    df = pd.read_csv(TEAMS_SEASONS_LINK_PATH, sep="\t")

    teams_link_set = set()
    
    for idx, row in df.iterrows():
        team_link = '/'.join(row['url'].split('/')[:5])
        teams_link_set.add(team_link)

    for team_link in teams_link_set:
        print(team_link)
        print('---')
        save_link(team_link)
        
if __name__ == "__main__":
    download_links_from_index()
    
