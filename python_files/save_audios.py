import json
import os
from gtts import gTTS
from python_files.colors import Colors


def save_audios(clear, name: str, lang: str = 'en'):
    clear()

    dir_path = f'./audios/{name}'

    # create file
    if os.path.exists(dir_path):
        pass
    else:
        os.mkdir(dir_path)

    # loading the json files
    with open(f'./json_files/{name}.json', 'r') as f:
        quiz_data = json.load(f)

    # save audio
    for q in quiz_data['questions']:
        quest_text = q['quest']
        quest_id = q['id']

        audio = gTTS(text=quest_text, lang=lang, slow=False)
        audio_path = f'{quest_id}.mp3'

        # save question audio
        print(f'{Colors.WARNING}Saving {audio_path}...')
        audio.save(f'./audios/{name}/{audio_path}')

        for a in q['answers']:
            ans_text = a['ans']

            # checking if answer text exists
            if ans_text is None:
                pass
            else:
                ans_id = a['id']

                audio = gTTS(text=ans_text, lang=lang, slow=False)
                audio_path = f'{ans_id}.mp3'

                # save answer audio
                print(f'{Colors.WARNING}Saving {audio_path}...')
                audio.save(f'./audios/{name}/{audio_path}')

    input(f'{Colors.OKGREEN}\nAll files are saved successfully, enter to continue: ')
