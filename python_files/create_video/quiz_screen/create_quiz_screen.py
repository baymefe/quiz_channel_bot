import json
from moviepy.editor import *
from python_files.colors import Colors
from python_files.create_video.quiz_screen.create_question_text import create_question_text
from python_files.create_video.quiz_screen.create_answer_text import create_answer_text
from python_files.create_video.quiz_screen.create_picture import create_picture
from python_files.create_video.quiz_screen.create_countdown import create_countdown


def get_quiz_bg_path(template: str, ans_type: str):
    return f'./resource/{template}/quiz_bg_{ans_type}.png'


def create_quiz_screen(configuration, question_data, json_name, template):
    # set duration: start break - q reading - guess break - a reading - end break
    duration = 10

    # get question id
    q_id = question_data['id']

    video_elements = []

    # set font color
    with open(f'./resource/{template}/font_color.json') as f:
        data = json.load(f)

    font_color = data['font_color']

    # creating question text
    question_text = create_question_text(
        configuration=configuration,
        question_data=question_data,
        json_name=json_name,
        font_color=font_color
    )
    video_elements.extend(question_text['clip'])

    # # create answers
    # get the number of answers
    ans_number = len(question_data['answers'])
    ans_type = '4_answers'
    if ans_number == 2:
        ans_type = '2_answers'
    elif ans_number == 3:
        ans_type = '3_answers'

    for i, answer in enumerate(question_data['answers']):

        # checking is the answer is text or image
        if answer['ans']:
            answer_text = create_answer_text(
                configuration=configuration,
                answer_data=answer,
                json_name=json_name,
                font_color=font_color,
                q_audio_end_time=question_text['audio_end'],
                answer_type=ans_type,
                i=i
            )

            # adding answers to clip
            video_elements.extend(answer_text['clip'])

            # duration
            if answer_text['duration'] > duration:
                duration = answer_text['duration']
        else:
            #image answers
            pass

    # create countdown
    countdown = configuration['quiz_screen']['timing']['guess_break']
    for c in range(countdown):
        cooldown_clip = create_countdown(
            configuration=configuration,
            font_color=font_color,
            start_time=question_text['audio_end'],
            text=str(countdown-c),
            additional_time=c
        )
        video_elements.append(cooldown_clip)

    # create background
    bg_path = get_quiz_bg_path(template, ans_type)
    quiz_background_clip = ImageClip(img=bg_path).set_duration(duration)
    video_elements.insert(0, quiz_background_clip)

    # create picture if it exists
    if question_data['picture_url'] is None:
        pass
    else:
        picture_clip = create_picture(
            configuration=configuration,
            image_path=f'./images/{json_name}/{q_id}.png',
            duration=duration
        )

        video_elements.append(picture_clip)

    # video elements to composite
    final_video = CompositeVideoClip(video_elements).set_duration(duration)

    return final_video
