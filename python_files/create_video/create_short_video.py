import json
from moviepy.editor import *
from python_files.create_video.quiz_screen.create_quiz_screen import create_quiz_screen


def create_short_video(clear, json_name):
    with open('./resource/short_video_configuration.json', 'r') as f:
        configuration = json.load(f)

    with open(f'./json_files/{json_name}.json', 'r') as f:
        data = json.load(f)

    video_clips = []

    # setting the name of the video
    video_name = input('Enter the video name: ')

    # get background
    print(f'Enter the quiz template. Bg file should be in the resource')
    background_path = input('Background name (short_template01): ') or 'short_template01'

    first_q_number = int(input('Plase enter the FIRST question number (0 is al questions): '))
    last_q_number = int(input('Plase enter the LAST question number (0 is al questions): '))

    if last_q_number == 0:

        # #  create multiple quiz screens
        print('creating multiple quiz screens')
        for question in data['questions']:
            quiz_clip = create_quiz_screen(
                configuration=configuration,
                question_data=question,
                json_name=json_name,
                template=background_path
            )
            video_clips.append(quiz_clip)
    else:
        # create single quiz screen
        print('creating quiz screen intervall')
        for i in range(first_q_number, last_q_number + 1):
            quiz_clip = create_quiz_screen(
                configuration=configuration,
                question_data=data['questions'][i-1],
                json_name=json_name,
                template=background_path
            )
            video_clips.append(quiz_clip)

    final_video = concatenate_videoclips(video_clips)

    # writing the video file
    final_video.write_videofile(f'./created_videos/{video_name}.mp4', fps=5)

    input('Enter to continue: ')
