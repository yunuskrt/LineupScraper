import json
import pandas as pd
from config import MATCH_PARSED_DATA_PATH, MANAGERS_LINK_PATH

ENCODING = "utf-8"

def check_exists():
    line_count = 0
    managers_set = set()
    with open(MATCH_PARSED_DATA_PATH, "r", encoding=ENCODING) as f:
        for line in f:
            line_count += 1
            line_data = json.loads(line)
            managers_set.add(line_data['home']['manager']['link'])
            managers_set.add(line_data['away']['manager']['link'])
    
    managers_df = pd.read_csv(MANAGERS_LINK_PATH, sep="\t")
    managers_links_set = set(managers_df['link'])

    if managers_set == managers_links_set:
        print("All manager links are in the parsed data.")
    else:
        print("Some manager links are not in the parsed data.")

if __name__ == "__main__":
    check_exists()

    
