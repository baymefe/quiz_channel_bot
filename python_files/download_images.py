import requests
import json
import os
from python_files.colors import Colors


def fetch_and_save_image(url: str, img_id: str, name: str):
    if url:
        image_source = requests.get(url)

        if image_source:
            dir_path = f'./images/{name}'
            path = f'./images/{name}/{img_id}.png'

            # create file
            if os.path.exists(dir_path):
                pass
            else:
                os.mkdir(dir_path)

            with open(path, 'wb') as f:
                f.write(image_source.content)

            print(f'{Colors.WARNING}Saving {img_id}.png...')

    pass


def download_images(clear, name: str):
    clear()

    # loading the json file
    with open(f'./json_files/{name}.json', 'r') as f:
        quiz_data = json.load(f)

    # get images
    for q in quiz_data['questions']:
        # question images
        quest_img_url = q['picture_url']
        if quest_img_url:
            quest_img_url = quest_img_url.split('?')[0]

        quest_img_id = q['id']

        fetch_and_save_image(quest_img_url, quest_img_id, name)

        for a in q['answers']:
            ans_img_url = a['picture_url']
            if ans_img_url:
                ans_img_url = ans_img_url.split('?')[0]

            ans_img_id = a['id']

            fetch_and_save_image(ans_img_url, ans_img_id, name)

    input(f'{Colors.OKGREEN}All pictures are saved successfully, enter to continue: ')
