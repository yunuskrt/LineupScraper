import os
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import uuid
from config import MATCH_LIST_PATH

ENCODING = "utf-8"

def save_link(url, season, page):
    # Save collected link/url and page to the .txt file in MATCH_LIST_PATH
 
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    league = 'Premier League'
    with open(MATCH_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, league, season, url, str(page)]) + "\n")

def download_links_from_index():
    # This function should go to the defined "url" and 
    # download the news page links from all pages and save them into a .txt file.
    
    # Checking if the match_list.txt file exists
    if not os.path.exists(MATCH_LIST_PATH):
        with open(MATCH_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "league", "season", "url", "page"]) + "\n")
        start_page = 0
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(MATCH_LIST_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 0
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max() + 1
            downloaded_url_list = data["url"].to_list()
    
    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    # time you ran the code (if you had an error and the code stopped)

    
    baseURL = "https://www.transfermarkt.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    important_teams = ['Man City', 'Arsenal', 'Tottenham', 'Chelsea', 'Liverpool', 'Man Utd']
    # season = '2022/2023'
    for saison in range(2009,2006,-1):
        season = '{}/{}'.format(saison,saison+1)
        print("Season",season)
        for page_id in range(1,39):
            print("Week",page_id)
            
            url = baseURL + "/premier-league/spieltag/wettbewerb/GB1/plus/?saison_id={}&spieltag={}".format(saison,page_id)
            resp = requests.get(url, headers=headers)
            soup = bs(resp.text, 'html.parser')
            
            match_rows = soup.find_all('tr',{'class':'table-grosse-schrift'})
            for match_row in match_rows:
                home_team = match_row.find('td',{'class':'rechts hauptlink no-border-rechts hide-for-small spieltagsansicht-vereinsname'}).find('a').text
                away_team = match_row.find('td',{'class':'hauptlink no-border-links no-border-rechts hide-for-small spieltagsansicht-vereinsname'}).find('a').text
                
                if any((home_team == team or away_team == team) for team in important_teams):
                    try:
                        match_href = match_row.find('span',{'class':'ergebnis-box'}).find('a')['href']
                        match_url = baseURL + match_href
                        print("Writing {} vs {}".format(home_team, away_team))
                        print('-'*50)
                        save_link(match_url,season, page_id)
                    except Exception as e:
                        print(f"Season: {season}, Week: {page_id}, HomeTeam: {home_team}, AwayTeam: {away_team}, Error: {e}")
    
if __name__ == "__main__":
    download_links_from_index()