from config import IMAGE_LINKS_PATH,PLAYERS_PARSED_DATA_PATH,TEAMS_PARSED_DATA_PATH,MANAGERS_PARSED_DATA_PATH
import json
import uuid
import pandas as pd
import os

ENCODING = "utf-8"
def save_link(url):
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(IMAGE_LINKS_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, url]) + "\n")

def download_image_links():
    if not os.path.exists(IMAGE_LINKS_PATH):
        with open(IMAGE_LINKS_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url"]) + "\n")
        start_page = 0
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(IMAGE_LINKS_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 0
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max() + 1
            downloaded_url_list = data["url"].to_list()

    image_links = set()
    
    # read player images
    with open(PLAYERS_PARSED_DATA_PATH, 'r') as f:
        for line in f:
            player = json.loads(line)
            image_links.add(player['image'])
    
    # read team images
    with open(TEAMS_PARSED_DATA_PATH, 'r') as f:
        for line in f:
            team = json.loads(line)
            image_links.add(team['image'])

    # read manager images
    with open(MANAGERS_PARSED_DATA_PATH, 'r') as f:
        for line in f:
            manager = json.loads(line)
            image_links.add(manager['image'])

    for image_link in image_links:
        save_link(image_link)
    print("Downloaded image links")
    print(len(image_links))

if __name__ == '__main__':
    download_image_links()