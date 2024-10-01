import os
import json
import re

from bs4 import BeautifulSoup as bs
from config import RAW_HTML_DIR, PARSED_HTML_PATH


# Encoding for writing the parsed data to JSONS file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"

def extract_content_from_page(file_path):
    playerRec = {
        'name': None, #string!
        'image': None, #string! 
        'date_of_birth': None, #string!
        'citizenship': None, #string?
        'height': None, #int?
        'position': None, #string?
        'foot': None, #string?
    }
    soup = bs(open(file_path, 'r').read(), 'html.parser')

    # Find header box
    try:
        headerBox = soup.find('header',{'class':'data-header'})
    except:
        return {'type':None,'msg':'headerBox not found'}
    
    # Find player name
    try:
        headlineElement = headerBox.find('div',{'class':'data-header__headline-container'}).find('h1',{'class':'data-header__headline-wrapper'})
        player_name = headlineElement.text.replace('\n','').strip()
    
        # exclude shirt number
        numElement = headlineElement.find('span',{'class':'data-header__shirt-number'})
        if numElement:
            player_name = player_name.replace(numElement.text.strip(),'')
        
        player_name = player_name.strip()
        playerRec['name'] = player_name
    except:
        return {'type':None,'msg':'player name not found'}
    
    # Find player image
    try:
        playerRec['image'] = headerBox.find('div',{'class':'data-header__profile-container'}).find('img')['src']
    except:
        return {'type':None,'msg':'player citizenship not found'}
    
    # Find info box
    try:
        infoBox = headerBox.find('div',{'class':'data-header__info-box'})
    except:
        return {'type':None,'msg':'infoBox not found'}
    
    # Find player date of birth and citizenship elements
    try:
        dateOfBirthElement = None
        citizenshipElement = None
        info_labels = infoBox.find_all('li',{'class':'data-header__label'})
        for info_label in info_labels:
            label_text = info_label.text.replace('\n','').strip().lower()
            if 'date of birth' in label_text:
                dateOfBirthElement = info_label
            elif 'citizenship' in label_text:
                citizenshipElement = info_label
            
            if dateOfBirthElement and citizenshipElement:
                break
    except:
        return {'type':None,'msg':'player date of birth or citizenship elements not found'}
    
    # Find player date of birth and citizenship
    try:
        date_of_birth = dateOfBirthElement.find('span',{'class':'data-header__content'})
        date_of_birth_text = date_of_birth.text.replace('\n','').strip()
        date_part = re.match(r'^[^(]+', date_of_birth_text).group().strip()
        
        playerRec['date_of_birth'] = date_part

        citizenship = citizenshipElement.find('span',{'class':'data-header__content'})
        citizenship_text = citizenship.text.replace('\n','').strip()
        
        playerRec['citizenship'] = citizenship_text
    except:
        return {'type':None,'msg':'player date of birth not found'}
    
    # Find player data box
    try:
        player_data_boxes = soup.find_all('div',{'class':'box viewport-tracking'})
        
        playerDataBoxCheck = True
        
        playerDataBox = None
        for header_box in player_data_boxes:
            boxElement = header_box.find('h2',{'class':'content-box-headline'})
            if boxElement:
                if 'player data' in boxElement.text.lower():
                    playerDataBox = header_box

        if playerDataBox is None:
            for header_box in player_data_boxes:
                boxElement = header_box.find('span',{'class':'content-box-headline'})
                if boxElement:
                    if 'player data' in boxElement.text.lower():
                        playerDataBox = header_box
        
        if playerDataBox is None:
            playerDataBoxCheck = False
    except:
        playerDataBoxCheck  = False
    
    # Find player height, position and foot
    try:
        if playerDataBoxCheck:
            player_info_table = None
            player_info_table = playerDataBox.find('div',{'class':'info-table info-table--right-space'})
            if player_info_table is None:
                player_info_table = playerDataBox.find('div',{'class':'info-table info-table--right-space min-height-audio'})

            player_infos = player_info_table.find_all('span')
            
            player_info_texts = []
            for player_info in player_infos:
                player_info_texts.append(player_info.text.replace('\n','').strip())

            heightVal = None
            positionVal = None
            footVal = None
            for i in range(len(player_info_texts)-1):
                label_text = player_info_texts[i].lower()
                if label_text.endswith(':'):
                    if 'height' in label_text and heightVal is None:
                        height_text = player_info_texts[i+1].replace(',','.').replace('\xa0','').replace('m','')
                        try:
                            if height_text == 'N/A':
                                playerRec['height'] = None
                            else:
                                playerRec['height'] = int(float(height_text)*100)
                            heightVal = True
                        except Exception as e:
                            playerRec['height'] = None

                    elif 'position' in label_text and positionVal is None:
                        position_text = player_info_texts[i+1]
                        if position_text == 'N/A':
                            playerRec['position'] = None
                        else:
                            playerRec['position'] = position_text
                        positionVal = True

                    elif 'foot' in label_text and footVal is None:
                        foot_text = player_info_texts[i+1]
                        if foot_text == 'N/A':
                            playerRec['foot'] = None
                        else:
                            playerRec['foot'] = foot_text
                        footVal = True
    except:
        return {'type':None,'msg':'player height, position or foot not found'}
    
    return playerRec    
    
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
    
        print(errorIds)
            

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
