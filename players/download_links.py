import os
import json
import pandas as pd
import uuid

from config import PLAYERS_LINK_PATH, MATCH_PARSED_DATA_PATH

ENCODING = "utf-8"


def save_link(link):
    # Save collected link/url and page to the .txt file in MATCH_LIST_PATH
 
    baseUrl = "https://www.transfermarkt.com"
    url = baseUrl + link
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(PLAYERS_LINK_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, link, url]) + "\n")

def download_links_from_index():

    # This function should go to the defined "url" and 
    # download the news page links from all pages and save them into a .txt file.
    
    # Checking if the players_list.txt file exists
    if not os.path.exists(PLAYERS_LINK_PATH):
        with open(PLAYERS_LINK_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "link", "url"]) + "\n")
        start_page = 0
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(PLAYERS_LINK_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 0
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max() + 1
            downloaded_url_list = data["url"].to_list()
    
    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    # time you ran the code (if you had an error and the code stopped)


    # Read the parsed transfermarkt data
    player_keys = set(['number','name','link','position','actions'])
    check = True
    line_count = 0
    with open(MATCH_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
        for line in f:
            line_count += 1
            line_data = json.loads(line)
            homeFirstPlayer = set(line_data['home']['first11'][0].keys())
            homeFirstSubPlayer = set(line_data['home']['substitutes'][0].keys())
            awayFirstPlayer = set(line_data['away']['first11'][0].keys())
            awayFirstSubPlayer = set(line_data['away']['substitutes'][0].keys())
            if homeFirstPlayer != player_keys or homeFirstSubPlayer != player_keys or awayFirstPlayer != player_keys or awayFirstSubPlayer != player_keys:
                check = False
                break
              
    if check:
        players_data_set = set()
        with open(MATCH_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
            for line in f:
                line_data = json.loads(line)
                homeFirst11 = line_data['home']['first11']
                homeSubstitutes = line_data['home']['substitutes']
                awayFirst11 = line_data['away']['first11']
                awaySubstitutes = line_data['away']['substitutes']
                for player in homeFirst11:
                    players_data_set.add(player['link'])
                for player in homeSubstitutes:
                    players_data_set.add(player['link'])
                for player in awayFirst11:
                    players_data_set.add(player['link'])
                for player in awaySubstitutes:
                    players_data_set.add(player['link'])

        print(len(players_data_set))

        for player_link in players_data_set:
            save_link(player_link)
        print("The links are saved to the file.")

    else:
        print("The data is not in the correct format. Line number: ", line_count)

if __name__ == "__main__":
    download_links_from_index()
