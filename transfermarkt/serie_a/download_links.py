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
    league = 'Serie A'
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
    important_teams = ['Inter','AS Roma','SSC Napoli','AC Milan','Juventus']
    relevant_teams = ['Inter','AS Roma','SSC Napoli','AC Milan','Juventus', 'Fiorentina','Atalanta BC','Lazio']

    for saison in range(2011,2006,-1):
        season = '{}/{}'.format(saison,saison+1)
        url = baseURL + "/serie-a/gesamtspielplan/wettbewerb/IT1?saison_id={}".format(saison)
        resp = requests.get(url, headers=headers)
        soup = bs(resp.text, 'html.parser')

        print('Writing Season',season)
        print('-'*30)

        containerBoxes = soup.find_all('div',{'class':'large-12 columns'})
        for containerBox in containerBoxes:
            matchBoxes = containerBox.select('div[class^="large-6 columns"]')
            for matchBox in matchBoxes:
                matchDay = matchBox.find('div',{'class':'content-box-headline'}).text
            
                matches = matchBox.find('tbody').find_all('tr')
                match_rows =[tr for tr in matches if not tr.get('class') or 'bg_blau_20' not in tr.get('class')]
                
                for match_row in match_rows:
                    home_team = match_row.find('td',{'class':'text-right no-border-rechts hauptlink'}).find('a').text
                    away_team = match_row.find('td',{'class':'no-border-links hauptlink'}).find('a').text
                    
                    if (home_team in important_teams and away_team in relevant_teams) or (away_team in important_teams and home_team in relevant_teams):
                        match_link = match_row.find('td',{'class':'zentriert hauptlink'}).find('a',{'class':'ergebnis-link'})['href']
                        print(matchDay,'->',home_team,'-',away_team)
                        print('*'*30)
                        save_link(baseURL+match_link,season,saison)
        
if __name__ == "__main__":
    download_links_from_index()