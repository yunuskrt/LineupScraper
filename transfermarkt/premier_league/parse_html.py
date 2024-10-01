import os
import json
from bs4 import BeautifulSoup as bs
from config import RAW_HTML_DIR, PARSED_HTML_PATH

# Encoding for writing the parsed data to JSONS file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"

def extract_content_from_page(file_path):
    soup = bs(open(file_path, 'r').read(), 'html.parser')

    matchRec = {
        'home': {
            'name': None, #string
            'link': None, #string
            'position': None,#int
            'score': None, #int
            'halfScore': None, #string
            'first11': None, #[{no:int, name:string,  link: string, position: string, actions:[]}]
            'substitutes': None, #[{no:int, name:string,  link: string, position: string, actions:[]}]
            'lineup': None, #string
            'manager': None # {name: string, link: string}
         },
         'away': {
            'name': None, #string
            'link': None, #string
            'position': None,#int
            'score': None, #int
            'halfScore': None, #string
            'first11': None, #[{no:int, name:string,  link: string, position: string, actions:[]}]
            'substitutes': None, #[{no:int, name:string,  link: string, position: string, actions:[]}]
            'lineup': None, #string
            'manager': None # {name: string, link: string}
         },
        'round': None, #string
        'date': None, #string
        'stadium': None, #string
        'attendance': None, #int
        'referee': None, #string
    }

    try:
        headerBox = soup.find('div',{'class':'box-content'})
        
        homeBox = headerBox.find('div',{'class':'sb-team sb-heim'}) # homeName, homeLink, homePosition
        homeLink = homeBox.find('a',{'class':'sb-vereinslink'})
        matchRec['home']['name'],matchRec['home']['link'] = homeLink.text,homeLink['href']
    except Exception as e:
        return {'type':None, 'msg': 'homeName or homeLink Error'}
    
    try:
        home_position = homeBox.find('p').text.replace(' ', '')
        if home_position.lower().startswith('position'):
            matchRec['home']['position'] = int(home_position[9:])
        scoreBox = headerBox.find('div',{'class':'sb-spieldaten'}) # round,date,homeScore,awayScore,homeHalfScore,awayHalfScore,stadium,attendance,referee
        dateInfo = scoreBox.find('p',{'class':'sb-datum hide-for-small'}).text.translate(str.maketrans('', '', ' \n\xa0')).split('|') # round, date
        matchRec['round'], matchRec['date'] = dateInfo[0], ' '.join(dateInfo[1:])
    except Exception as e:
        return {'type':None, 'msg':'round or date Error'}
    
    try:
        scoreInfo = scoreBox.find('div',{'class':'sb-endstand'}) # homeScore, awayScore
        matchScore = scoreInfo.contents[0].translate(str.maketrans('', '', ' \n')).split(':')
        matchRec['home']['score'], matchRec['away']['score'] = int(matchScore[0]), int(matchScore[1])
    except Exception as e:
        return {'type':None, 'msg': 'homeScore or awayScore Error'}
    
    try:
        halfScore = scoreInfo.find('div',{'class':'sb-halbzeit'}).text[1:-1].split(':') # homeHalfScore, awayHalfScore
        matchRec['home']['halfScore'], matchRec['away']['halfScore'] = int(halfScore[0]), int(halfScore[1])
    except Exception as e:
        return {'type': None, 'msg': 'homeHalfScore or awayHalfScore Error'}
    
    try:
        additionalInfos = scoreBox.find('p',{'class':'sb-zusatzinfos'})
        stadiumInfo = additionalInfos.find('span',{'class':'hide-for-small'}) # stadium, attendance, referee
        
        matchRec['stadium']  = stadiumInfo.find('a').text

        matchAttendance = stadiumInfo.find('strong')
        if matchAttendance is not None:
            matchRec['attendance'] = int(''.join([char for char in matchAttendance.text if char.isdigit()]))
        
        matchRec['referee'] = additionalInfos.find_all('a')[-1].text
    except Exception as e:
        return {'type': None, 'msg': 'stadium, attendance or referee Error'}
    
    try:
        awayBox = headerBox.find('div',{'class':'sb-team sb-gast'}) # awayName, awayLink, awayPosition
        awayLink = awayBox.find('a',{'class':'sb-vereinslink'})
        matchRec['away']['name'], matchRec['away']['link'] = awayLink.text, awayLink['href']
        
        away_position = homeBox.find('p').text.replace(' ', '')
        if away_position.lower().startswith('position'):
            matchRec['away']['position'] = int(away_position[9:])
    except Exception as e:
        return {'type': None, 'msg': 'awayName, awayLink or awayPosition Error'}

    try:
        headlineBoxes = soup.find_all('h2',{'class':'content-box-headline'})
        lineupBox = None
        for i in headlineBoxes:
            if 'line' in i.text.lower() and 'up' in i.text.lower():
                lineupBox = i.parent
                break
    except Exception as e:
        return {'type': None, 'msg': 'lineupBox not found Error'}
    
    try:
        homeLineupBox = lineupBox.find('div',{'class':'large-6 columns aufstellung-box'})
        matchRec['home']['lineup'] = homeLineupBox.find('div',{'class':'large-7 aufstellung-vereinsseite columns small-12 unterueberschrift aufstellung-unterueberschrift'}).text.translate(str.maketrans('', '', ' \n')).split(':')[1]
    except Exception as e:
        return {'type': None, 'msg': 'homeLineup Error'}
    
    try:
        home11Elements = homeLineupBox.find_all('div',{'class':'aufstellung-spieler-container'})
        homeFirstElevenPlayers = []
        for player in home11Elements:
            # {number:int, name:string,  link: string, position: string,actions:[]}
            number = int(player.find('div',{'class':'tm-shirt-number tm-shirt-number--large tm-shirt-number--bordered'}).text.translate(str.maketrans('', '', ' \n')))
            playerElement = player.find('span',{'class':'aufstellung-rueckennummer-name'}).find('a')
            name,link = playerElement.text, playerElement['href']
            position = player['style'].replace(' ','')[:-1]
    
            actions = []
            if (player.find('div',{'class':'kapitaenicon-formation'})):
                actions.append('captain')
            actionElements = player.select("span[class^='icons_sprite']")
            for action in actionElements:
                actionList = action['class']
                if 'icon-gelbekarte-formation' in actionList:
                    actions.append('yellow')
                if 'icon-rotekarte-formation' in actionList:
                    actions.append('red')
                if 'icon-gelbrotekarte-formation' in actionList:
                    actions.append('yellow-red')
                if 'icon-auswechslung-formation' in actionList:
                    actions.append('sub-out')
                if 'icon-tor-formation' in actionList:
                    actions.append('goal')
            homeFirstElevenPlayers.append({'number':number,'name':name,'link':link,'position':position,'actions':actions})
        matchRec['home']['first11'] = homeFirstElevenPlayers
    except Exception as e:
        return {'type': None, 'msg': 'homeFirst11 Error'}
    
    try:
        homeSubstitutes = homeLineupBox.find('table',{'class':'ersatzbank'}).find_all('tr')
        homeManager, homeSubPlayerList = homeSubstitutes[-1].find('a'),homeSubstitutes[:-1]
        matchRec['home']['manager'] = {'name':homeManager.text,'link':homeManager['href']}
    except Exception as e:
        return {'type': None, 'msg': 'homeManager Error'}

    try:
        homeSubstitutePlayers = []
        for player in homeSubPlayerList:
            # [{number:int, name:string,  link: string, position: string, actions:[]}]
            number = int(player.find('div',{'class':'tm-shirt-number tm-shirt-number--small'}).text)
            
            playerElement = player.find('a')
            name,link = playerElement.text, playerElement['href']

            position = player.find_all('td')[-1].text.translate(str.maketrans('', '', ' \n'))

            actions = []
            actionElements = player.select("span[class^='icons_sprite']")

            for action in actionElements:
                actionList = action['class']
                if 'icon-gelbekarte-formation' in actionList:
                    actions.append('yellow')
                if 'icon-rotekarte-formation' in actionList:
                    actions.append('red')
                if 'icon-gelbrotekarte-formation' in actionList:
                    actions.append('yellow-red')
                if 'icon-auswechslung-formation' in actionList:
                    actions.append('sub-out')
                if 'icon-einwechslung-formation' in actionList:
                    actions.append('sub-in')
                if 'icon-tor-formation' in actionList:
                    actions.append('goal')
            
            homeSubstitutePlayers.append({'number':number,'name':name,'link':link,'position':position, 'actions':actions})
        matchRec['home']['substitutes'] = homeSubstitutePlayers
    except Exception as e:
        return {'type': None, 'msg': 'Home Substitutes Error'}

    try:
        awayLineupBox = lineupBox.find('div',{'class':'large-6 columns'})
        matchRec['away']['lineup'] = awayLineupBox.find('div',{'class':'large-7 aufstellung-vereinsseite columns small-12 unterueberschrift aufstellung-unterueberschrift'}).text.translate(str.maketrans('', '', ' \n')).split(':')[1]
    except Exception as e:
        return {'type': None, 'msg': 'awayLineup Error'}
    
    try: 
        away11Elements = awayLineupBox.find_all('div',{'class':'aufstellung-spieler-container'})
        awayFirstElevenPlayers = []
        for player in away11Elements:
            # {number:int, name:string,  link: string, position: string,actions:[]}
            number = int(player.find('div',{'class':'tm-shirt-number tm-shirt-number--large tm-shirt-number--bordered'}).text.translate(str.maketrans('', '', ' \n')))
            
            playerElement = player.find('span',{'class':'aufstellung-rueckennummer-name'}).find('a')
            name,link = playerElement.text, playerElement['href']
            
            position = player['style'].replace(' ','')[:-1]

            actions = []
            if (player.find('div',{'class':'kapitaenicon-formation'})):
                actions.append('captain')
            actionElements = player.select("span[class^='icons_sprite']")

            for action in actionElements:
                actionList = action['class']
                if 'icon-gelbekarte-formation' in actionList:
                    actions.append('yellow')
                if 'icon-rotekarte-formation' in actionList:
                    actions.append('red')
                if 'icon-gelbrotekarte-formation' in actionList:
                    actions.append('yellow-red')
                if 'icon-auswechslung-formation' in actionList:
                    actions.append('sub-out')
                if 'icon-tor-formation' in actionList:
                    actions.append('goal')

            awayFirstElevenPlayers.append({'number':number,'name':name,'link':link,'position':position,'actions':actions})
        matchRec['away']['first11'] = awayFirstElevenPlayers
    except Exception as e:
        return {'type': None, 'msg': 'awayFirst11 Error'}

    try:
        awaySubstitutes = awayLineupBox.find('table',{'class':'ersatzbank'}).find_all('tr')
        awayManager, awaySubPlayerList = awaySubstitutes[-1].find('a'),awaySubstitutes[:-1]

        matchRec['away']['manager'] = {'name':awayManager.text,'link':awayManager['href']}
    except Exception as e:
        return {'type': None, 'msg': 'awayManager Error'}    
    
    try:
        awaySubstitutePlayers = []
        for player in awaySubPlayerList:
            # [{number:int, name:string,  link: string, position: string, actions:[]}]
            number = int(player.find('div',{'class':'tm-shirt-number tm-shirt-number--small'}).text)

            playerElement = player.find('a')
            name,link = playerElement.text, playerElement['href']

            position = player.find_all('td')[-1].text.translate(str.maketrans('', '', ' \n'))

            actions = []
            actionElements = player.select("span[class^='icons_sprite']")
            for action in actionElements:
                actionList = action['class']
                if 'icon-gelbekarte-formation' in actionList:
                    actions.append('yellow')
                if 'icon-rotekarte-formation' in actionList:
                    actions.append('red')
                if 'icon-gelbrotekarte-formation' in actionList:
                    actions.append('yellow-red')
                if 'icon-auswechslung-formation' in actionList:
                    actions.append('sub-out')
                if 'icon-einwechslung-formation' in actionList:
                    actions.append('sub-in')
                if 'icon-tor-formation' in actionList:
                    actions.append('goal')

            awaySubstitutePlayers.append({'number':number,'name':name,'link':link,'position':position, 'actions':actions})
        matchRec['away']['substitutes'] = awaySubstitutePlayers
    except Exception as e:
        return {'type': None, 'msg': 'Away Substitutes Error'}

    return matchRec
    
    
    
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
            

            #### REMOVE ERROR FILES
            # # Specify the path to the file
            # file_path = os.path.join(RAW_HTML_DIR, id[0] + '.html')
            
            # # Check if the file exists
            # if os.path.exists(file_path):
            #     os.remove(file_path)
            #     print(f"{id}.html removed successfully")
            # else:
            #     print(f"{id}.html does not exist")

            # print('*'*40)

if __name__ == "__main__":
    parse_html_pages()