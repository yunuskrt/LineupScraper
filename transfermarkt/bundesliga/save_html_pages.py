import os
import requests
import pandas as pd
from config import MATCH_LIST_PATH, RAW_HTML_DIR


# Encoding for writing the page html files
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def get_page_content(page_url):
    """
    This function should take the URL of a page and return the html
    content (string) of that page.
    """

    # WRITE YOUR CODE HERE
    ###############################

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    resp = requests.get(page_url, headers=headers)
    if resp.status_code >= 200 and resp.status_code < 300:
        page_html = resp.text   
        # Save the page content (html) in the variable "page_html"

        ###############################
        return page_html
    else:
        raise "Page not parsed"

def save_html_pages():
    # Step 1: Read URL/Link list file from MATCH_LIST_PATH
    #         to get the urls that need to be saved
    url_df = pd.read_csv(MATCH_LIST_PATH, sep="\t")

    # Step 2: Checking the downloaded html page IDs
    html_list = os.listdir(RAW_HTML_DIR)
    id_list = list(map(lambda x: x[:-5], html_list))

    # Step 3: Iterating through the URL list
    for idx, row in url_df.iterrows():
        print('{} pages processed.'.format(idx))
        page_id = row["id"]
        page_url = row["url"]

        # Skip page if already downloaded
        if page_id in id_list:
            continue

        # Step 4: Loading page html
        loaded = True
        try:
            # Save the html content of the page in the variable page_html
            page_html = get_page_content(page_url)

        except Exception as e:
            # Pages that were not collected are saved as empty strings
            page_html = ""
            loaded = False
            print(f"Error getting page {page_id} html: {e}")

        # Step 5: Saving page html
        if loaded: # page content get from web
            try:
                save_path = os.path.join(RAW_HTML_DIR, f"{page_id}.html")

                with open(save_path, "w", encoding=ENCODING) as f:
                    f.write(page_html)
                print(f"Saved page {page_id} ({idx+1} / {url_df.shape[0]})")

            except Exception as e:
                with open(save_path, "w", encoding=ENCODING) as f:
                    f.write("")
                print("Error saving page {page_id} html:" + str(e))
        
if __name__ == "__main__":
    save_html_pages()