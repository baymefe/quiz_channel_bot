import json
import math
from gtts import gTTS
from moviepy.editor import *


def set_background(template):
    return ImageClip(img=f'./resource/{template}/title_screen.png')


def set_title_audio(json_name, title):
    audio = gTTS(text=title, lang='en', slow=False)
    audio.save(f'./audios/{json_name}/title.mp3')


def create_title_screen(configuration, json_name, template, title):
    # set configuration
    start_break = configuration['title_screen']['timing']['start_break']
    end_break = configuration['title_screen']['timing']['end_break']

    banner = configuration['title_screen']['banner']

    # set title audio
    set_title_audio(json_name, title)
    audio = AudioFileClip(filename=f'./audios/{json_name}/title.mp3').set_start(start_break)
    audio_duration = math.ceil(audio.duration)

    # get font color
    with open(f'./resource/{template}/font_color.json', 'r') as f:
        data = json.load(f)

    font_color = data['font_color']

    background_clip = set_background(template)
    background_clip = background_clip.set_duration(start_break + audio_duration + end_break)
    background_clip.audio = audio

    title_clip = (
        TextClip(
            txt=title,
            size=(banner['w'] - 2 * banner['px'], banner['h'] - 2 * banner['py']),
            color=font_color,
            font='Arial-Bold',
            method='caption'
        )
        .set_position((banner['x'] + banner['px'], banner['y'] + banner['py']))
        .set_duration(start_break + audio_duration + end_break)
    )

    final_clip = CompositeVideoClip([background_clip, title_clip])

    return final_clip
