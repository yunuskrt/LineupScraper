import os
import json
import re

from bs4 import BeautifulSoup as bs
from config import RAW_HTML_DIR, PARSED_HTML_PATH

# Encoding for writing the parsed data to JSONS file
ENCODING = "utf-8"

def extract_content_from_page(file_path):
    managerRec = {
        'name': None, #string!
        'image': None, #string!
        'date_of_birth': None, #string?
        'citizenship': None, #string?
    }
    soup = bs(open(file_path, 'r').read(), 'html.parser')
    
    # Find header box
    try:
        headerBox = soup.find('header',{'class':'data-header'})
    except:
        return {'type':None, 'msg':'headerBox not found'}
    
    # Find manager name
    try:
        nameElement = headerBox.find('div',{'class':'data-header__headline-container'}).find('h1',{'class':'data-header__headline-wrapper'})
        name_text = nameElement.text.replace('\n','').strip()
        managerRec['name'] = name_text
    except:
        return {'type':None, 'msg':'name not found'}
    
    # Find manager image
    try:
        managerRec['image'] = headerBox.find('div',{'class':'data-header__profile-container'}).find('img')['src']
    except:
        return {'type':None, 'msg':'image not found'}
    
    # Find info box
    try:
        infoBox = headerBox.find('div',{'class':'data-header__info-box'})
    except:
        return {'type':None, 'msg':'infoBox not found'}
    
    # Find date of birth and citizenship elements
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
        return {'type':None, 'msg':'date_of_birth or citizenship elements not found'}
    
    # Find player date of birth and citizenship
    try:
        if dateOfBirthElement:
            date_of_birth = dateOfBirthElement.find('span',{'class':'data-header__content'})
            date_of_birth_text = date_of_birth.text.replace('\n','').strip()
            date_part = re.match(r'^[^(]+', date_of_birth_text).group().strip()
            if date_part == 'N/A':
                managerRec['date_of_birth'] = None
            else:
                managerRec['date_of_birth'] = date_part

        if citizenshipElement:
            citizenship = citizenshipElement.find('span',{'class':'data-header__content'})
            if citizenship:
                citizenship_text = citizenship.text.replace('\n','').strip()
                if citizenship_text == 'N/A':
                    managerRec['citizenship'] = None
                else:
                    managerRec['citizenship'] = citizenship_text
    except:
        return {'type':None,'msg':'manager date of birth or citizenship not found'}
    
    return managerRec
    
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
