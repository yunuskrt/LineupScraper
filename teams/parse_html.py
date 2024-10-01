import os
import json
from bs4 import BeautifulSoup as bs
from config import RAW_HTML_DIR, PARSED_HTML_PATH

# Encoding for writing the parsed data to JSONS file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"

def extract_content_from_page(file_path):
    teamRec = {
        'name': None, # string!
        'image': None, # string!
        'stadium': {
            'name': None, # string?
            'capacity': None, # int?
        }, # string!
    }
    soup = bs(open(file_path, 'r').read(), 'html.parser')

    # Find header
    try:
        headerBox = soup.find('header',{'class':'data-header'})
    except:
        return {'type':None,'msg':'headerBox not found'}
    
    # Find team name
    try:
        teamName = headerBox.find('div',{'class':'data-header__headline-container'}).find('h1',{'class':'data-header__headline-wrapper data-header__headline-wrapper--oswald'}).text.strip()
        teamRec['name'] = teamName
    except:
        return {'type':None,'msg':'team name not found'}
    
    # Find team image
    try:
        teamImage = headerBox.find('div',{'class':'data-header__profile-container'}).find('img')['src']
        teamRec['image'] = teamImage
    except:
        return {'type':None,'msg':'team image not found'}
    
    # Find stadium name, capacity
    try:
        infoBox = headerBox.find('div',{'class':'data-header__info-box'})
        stadiumElement = None
        
        infoItems = infoBox.find_all('ul',{'class':'data-header__items'})
        break_check = False

        for info_item in infoItems:
            info_labels = info_item.find_all('li',{'class':'data-header__label'})
            
            for info_label in info_labels:
                label_text = info_label.get_text(strip=True, separator=' ').lower()
                if 'stadium' in label_text:
                    stadiumElement = info_label
                    break_check = True
                    break
            if break_check:
                break
                
        if stadiumElement:
            stadiumInfo = stadiumElement.find('span',{'class':'data-header__content'})
            
            teamRec['stadium']['name'] = stadiumInfo.find('a').text 
            
            capacityElement = stadiumInfo.find('span',{'class':'tabellenplatz'})
            if capacityElement:
                capacity_text = capacityElement.text
                seats_text = 'seats' if 'seats' in capacity_text else 'Seats' if 'Seats' in capacity_text else None
                
                if seats_text:
                    capacity_text = capacity_text.replace(seats_text,'')

                teamRec['stadium']['capacity'] = int(capacity_text.replace(',','').replace('.','').strip())
    
    except:
        return {'type':None,'msg':'stadium name or capacity not found'}
    
    return teamRec
   
    
    
    
def parse_html_pages():
    # Load the parsed pages
    parsed_id_list = []
    if os.path.exists(PARSED_HTML_PATH):
        with open(PARSED_HTML_PATH, "r", encoding=ENCODING) as f:
            # Saving the parsed ids to avoid reparsing them
            for line in f:
                data = json.loads(line.strip())
                id_str = data["id"]
                parsed_id_list.append(id_str)
    else:
        with open(PARSED_HTML_PATH, "w", encoding=ENCODING) as f:
            pass

    # Iterating through html files

    errorIds = []
    for file_name in os.listdir(RAW_HTML_DIR):
        page_id = file_name[:-5]

        # Skip if already parsed
        if page_id in parsed_id_list:
            continue

        # Read the html file and extract the required information

        # Path to the html file
        file_path = os.path.join(RAW_HTML_DIR, file_name)

        try:
            parsed_data = extract_content_from_page(file_path)
            if len(parsed_data.keys()) == 2:
                errorIds.append((page_id,parsed_data['msg']))
            else:
                parsed_data["id"] = page_id
                print(f"Parsed page {page_id}")

                # Saving the parsed data
                with open(PARSED_HTML_PATH, "a", encoding=ENCODING) as f:
                    f.write("{}\n".format(json.dumps(parsed_data)))

        except Exception as e:
            print(f"Failed to parse page {page_id}: {e}")
            errorIds.append(page_id)


    if len(errorIds) == 0:
        print('All pages parsed. No eror detected.')
    else:
        print('ERROR IDs')
        print('-'*40)
        for index,id in enumerate(errorIds):
            print(index+1,'->',id[0],'---',id[1])
            

            # ### REMOVE ERROR FILES
            # # Specify the path to the file

            # try:
            #     file_path = os.path.join(RAW_HTML_DIR, id[0] + '.html')
            #     # Check if the file exists
            #     if os.path.exists(file_path):
            #         os.remove(file_path)
            #         print(f"{id}.html removed successfully")
            #     else:
            #         print(f"{id}.html does not exist")

            #     print('*'*40)
            # except Exception as e:
            #     print(f"Failed to remove {id[0]}.html: {e}")
            #     print('*'*40)

        


if __name__ == "__main__":
    parse_html_pages()
    print(len(os.listdir(RAW_HTML_DIR)))
