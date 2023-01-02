from moviepy.editor import *


def create_countdown(configuration, start_time, text, font_color, additional_time):
    # set configuration
    countdown_box = configuration['count_down']

    #

    number_clip = (
        TextClip(
            txt=str(text),
            color='white',  # font_color,
            font='Arial-Bold',
            align='center',
            size=(countdown_box['w'], countdown_box['h']),
        )
        .set_duration(1)
        .set_position((countdown_box['x'], countdown_box['y']))
    )

    final_clip = number_clip.set_start(start_time + additional_time)

    return final_clip
