from moviepy.editor import *


def create_picture(configuration, image_path, duration):
    # assigning configuration
    image_config = {
        'h': configuration['quiz_screen']['image']['h'],
        'y': configuration['quiz_screen']['image']['y'],
    }
    screen_w = configuration['screen']['w']

    # get the image
    image = ImageClip(img=image_path).set_duration(duration)
    resized_image = image.resize(height=image_config['h'])

    # get set x pos
    width = resized_image.w
    x_pos = screen_w/2 - width/2

    final_image = resized_image.set_position((x_pos, image_config['y']))

    return final_image
