import os
import json
import pandas as pd
import uuid

from config import TEAMS_SEASONS_LINK_PATH, MATCH_PARSED_DATA_PATH

ENCODING = "utf-8"


def save_link(link):
    # Save collected link/url and page to the .txt file in MATCH_LIST_PATH
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, link).hex
    with open(TEAMS_SEASONS_LINK_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, link]) + "\n")

def download_links_from_index():

    # This function should go to the defined "url" and 
    # download the news page links from all pages and save them into a .txt file.
    
    # Checking if the players_list.txt file exists
    if not os.path.exists(TEAMS_SEASONS_LINK_PATH):
        with open(TEAMS_SEASONS_LINK_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url"]) + "\n")
        start_page = 0
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(TEAMS_SEASONS_LINK_PATH, sep="\t")
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
    check = True
    line_count = 0
    with open(MATCH_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
        for line in f:
            line_count += 1
            line_data = json.loads(line)
            homeLink, awayLink = line_data['home']['link'], line_data['away']['link']
            if homeLink is None or awayLink is None or homeLink == "" or awayLink == "":
                check = False
                print(homeLink, awayLink)
    if check:
        teams_data_set = set()
        with open(MATCH_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
            for line in f:
                line_data = json.loads(line)
                teams_data_set.add(line_data['home']['link'])
                teams_data_set.add(line_data['away']['link'])

        print(len(teams_data_set))
        for team_link in teams_data_set:
            save_link(team_link)
        print("The links are saved to the file.")

    else:
        print("The data is not in the correct format. Line number: ", line_count)

if __name__ == "__main__":
    download_links_from_index()
