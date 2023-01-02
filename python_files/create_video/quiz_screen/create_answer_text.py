from moviepy.editor import *


def create_answer_text(configuration, answer_data, json_name, font_color, q_audio_end_time, answer_type, i):
    # timing settings
    guess_break = configuration['quiz_screen']['timing']['guess_break']
    end_break = configuration['quiz_screen']['timing']['end_break']

    # get answer text and id
    answer_text = answer_data['ans']
    answer_id = answer_data['id']

    # assigning the configuration
    answers_config_general = configuration['quiz_screen'][f'size_{answer_type}']
    answers_config_individual = configuration['quiz_screen'][answer_type]

    a_box_config = {
        'x': answers_config_individual[i]['x'],
        'y': answers_config_individual[i]['y'],
        'w': answers_config_general['w'],
        'h': answers_config_general['h']
    }

    # answer configuration settings
    # set padding
    at_px = answers_config_general['px']
    at_py = answers_config_general['py']
    at_config = {
        'x': answers_config_individual[i]['x'] + at_px,
        'y': answers_config_individual[i]['y'] + at_py,
        'w': answers_config_general['w'] - 2 * at_px,
        'h': answers_config_general['h'] - 2 * at_py,
    }

    # set dur_time
    dur_time = 0

    if answer_data['check']:
        # get correct answer audio
        answer_audio = AudioFileClip(f'audios/{json_name}/{answer_id}.mp3')

        dur_time = end_break + round(answer_audio.duration)

        # create tick symbol
        correct_answer_clip = (
            ColorClip(
                size=(a_box_config['w'], a_box_config['h']),
                color=[20, 255, 0]
            )
            .set_position((a_box_config['x'], a_box_config['y']))
            .set_start(q_audio_end_time + guess_break)
            .set_duration(dur_time)
        )

        # add the answer audio
        correct_answer_clip.audio = answer_audio.set_start(q_audio_end_time + guess_break)
    else:
        correct_answer_clip = None

    # creating answer text clip
    answer_text_clip = (
        TextClip(
            txt=answer_text,
            color=font_color,
            method='caption',
            font='Arial-Bold',
            size=(at_config['w'], at_config['h'])
        ).set_position((at_config['x'], at_config['y']))
    )

    if correct_answer_clip:
        return {
            'clip': [correct_answer_clip, answer_text_clip],
            'duration': q_audio_end_time + guess_break + dur_time
        }

    else:
        return {
            'clip': [answer_text_clip],
            'duration': q_audio_end_time + guess_break + dur_time
        }
