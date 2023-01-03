# get a json file
import json
import pathlib
from time import sleep
from playwright.sync_api import sync_playwright
from python_files.colors import Colors
from typing import Callable


def fetch_data(url):
    print(f'{Colors.WARNING}Fetching started...')

    with sync_playwright() as p:
        # open browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url)

        sleep(2)

        # show answers
        show_answers = page.query_selector('xpath=//*[@id="root"]/div/div/div/main/div[2]/div[2]/div[2]/div/section[1]/div[1]/button')
        show_answers.click()

        # save title
        title = page.query_selector('xpath=//*[@id="root"]/div/div/div/main/div[2]/div[2]/div[1]/div[3]/div[1]').text_content()

        # save the publisher
        publisher = page.query_selector('xpath=/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[1]/div[3]/div[5]/div[2]/div/a').text_content()

        # get rid of the icon
        if publisher[0:4] == 'Icon':
            publisher = publisher.lstrip('Icon')

        # save tags
        tag_elements = page.query_selector_all('xpath=//*[@id="root"]/div/div/div/main/div[2]/div[2]/div[1]/div[3]/div[5]/span/child::a')

        tags = []

        for tag in tag_elements:
            tags.append(tag.text_content())

        # # save the questions
        question_elements = page.query_selector_all('xpath=/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[2]/div/section[1]/div[2]/child::div/div[1]')

        questions = []

        for i, q in enumerate(question_elements):
            question: object

            # the id of the question
            quest_id = hex(i)

            # get question type
            quest_type = q.query_selector('xpath=/div[1]/button/div/span/span[3]').text_content()

            # check if question or slide etc.
            if quest_type == 'Quiz' or quest_type == 'True or false':
                quest = q.query_selector('xpath=/div[1]/button/span').text_content()
                quest_pic_url = q.query_selector('xpath=/div[1]/div/div').get_attribute('title')

                # get answers
                answer_elements = q.query_selector_all('xpath=/div[2]/child::div')

                answers = []

                for j, a in enumerate(answer_elements):
                    # get the id of the answer
                    ans_id = f'{quest_id}_{hex(j)}'

                    # get area label
                    aria_label = a.get_attribute('aria-label')

                    # checking if the question is a picture
                    # here we assume that the answer can either be text or a picture
                    try:
                        ans = a.query_selector('xpath=/div/div[1]/span').text_content()
                    except:
                        # picture answer
                        ans_pic_url = a.query_selector('xpath=/div/div[1]/div[2]/div').get_attribute('title')
                        ans = None
                    else:
                        # text answer
                        ans_pic_url = None

                    check: bool

                    if 'correct' in aria_label:
                        check = True
                    if 'incorrect' in aria_label:
                        check = False

                    answer = {
                        "id": ans_id,
                        "ans": ans,
                        "check": check,
                        "picture_url": ans_pic_url
                    }

                    answers.append(answer)

                question = {
                    "id": quest_id,
                    "quest": quest,
                    "picture_url": quest_pic_url,
                    "type": quest_type,
                    "answers": answers
                }

                questions.append(question)

        print(f'{Colors.OKGREEN}\nAll questions are fetched successfully.')

        return {
            'title': title,
            'publisher': publisher,
            'tags': tags,
            'questions': questions
        }


def get_json_file(clear: Callable, url: str):
    clear()
    print(f'{url}\n')

    # url = 'https://create.kahoot.it/details/4c392408-9522-4a55-a796-8cce9aeaa515'
    # url = 'https://create.kahoot.it/details/2a213f96-b74b-498e-8e4c-93e842210e7d'

    data = fetch_data(url)

    # count the number of json files
    files = pathlib.Path('./json_files').iterdir()
    count_json = sum(map(lambda x: x.suffix == '.json', files))
    title = data['title']
    new_title = ''.join(filter(str.isalnum, title)).lower()

    json_name = f'Nr{count_json:04n}_{new_title}'

    with open(f'./json_files/{json_name}.json', 'w') as f:
        f.write(json.dumps(data, indent=2))

    print(f'{Colors.OKGREEN}The json file is saved successfully.')
    input('Enter to continue')

    return json_name
