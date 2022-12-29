from moviepy.editor import *
import math


def create_question_text(configuration, question_data, font_color, json_name):
    # assigning configuration
    banner_config = configuration['quiz_screen']['banner']

    question_text = question_data['quest']
    question_id = question_data['id']

    start_break = configuration['quiz_screen']['timing']['start_break']

    # # question text settings
    # set padding
    qt_px = banner_config['px']
    qt_py = banner_config['py']
    qt_config = {
        'x': banner_config['x'] + qt_px,
        'y': banner_config['y'] + qt_py,
        'w': banner_config['w'] - 2 * qt_px,
        'h': banner_config['h'] - 2 * qt_py,
    }

    # create question text
    question_text_clip = (
        TextClip(
            txt=question_text,
            color=font_color,
            method='caption',
            font='Arial-Bold',
            size=(qt_config['w'], qt_config['h'])
        ).set_position((qt_config['x'], qt_config['y']))
    )

    # create question audio
    question_audio = AudioFileClip(f'audios/{json_name}/{question_id}.mp3').set_start(start_break)
    # add the audio
    question_text_clip.audio = question_audio

    return {
        'clip':  [question_text_clip],
        # math.ceil because there is going to be ticking sound. they shouldn't overlap
        'audio_end': start_break + math.ceil(question_audio.duration)
    }
