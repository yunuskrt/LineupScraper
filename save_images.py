from config import DIR_IMAGES, IMAGE_LINKS_PATH
import requests
import os
import pandas as pd

def save_image(id,content):
    save_path = os.path.join(DIR_IMAGES, f"{id}.png")
    with open(save_path, "wb",) as f:
        f.write(content)

def get_image_content(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.content
        else:
            print("Failed to download image. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Failed to download image:", e)
        return None


def save_images():
    # Step 1: Read URL/Link list file from IMAGE_LINKS_PATH
    #         to get the urls that need to be saved
    url_df = pd.read_csv(IMAGE_LINKS_PATH, sep="\t")
    
    # Step 2: Checking the downloaded html page IDs
    html_list = os.listdir(DIR_IMAGES)
    id_list = list(map(lambda x: x[:-4], html_list))

    # Step 3: Iterating through the URL list
    count = 0
    error_list = []
    for idx, row in url_df.iterrows():
        print('{} pages processed.'.format(idx))
        id = row["id"]
        url = row["url"]

        # Skip page if already downloaded
        if id in id_list:
            continue

        # Step 4: Loading page html
        image_content = get_image_content(url)

        # Step 5: Saving page html
        if image_content is not None: # page content get from web
            try:
                count += 1
                print(f"Saved page {id} ({idx+1} / {url_df.shape[0]})")
                save_image(id,image_content)
                if count == 500:
                    break

            except Exception as e:
                error_list.append(id)
                print("Error saving page {page_id} html:" + str(e))
                break
        else:
            error_list.append(id)
    

    if len(error_list) > 0:
        print("Error ids:")
        for e in error_list:
            print(e)
            print('*'*40)
    else:
        print("No error detected this part.")
        
    # ### REMOVE ERROR FILES
    # # Specify the path to the file

    # for id in error_list:
    #     try:
    #         file_path = os.path.join(DIR_IMAGES, id + '.png')
    #         # Check if the file exists
    #         if os.path.exists(file_path):
    #             os.remove(file_path)
    #             print(f"{id}.png removed successfully")
    #         else:
    #             print(f"{id}.png does not exist")
    #         print('*'*40)
    #     except Exception as e:
    #         print(f"Failed to remove {id}.png: {e}")
    #         print('*'*40)

if __name__ == '__main__':
    save_images()
    print(len(os.listdir(DIR_IMAGES)))