import json
import math
from moviepy.editor import *
from python_files.colors import Colors
from python_files.create_video.quiz_screen.create_quiz_screen import create_quiz_screen
from python_files.create_video.create_title_screen import create_title_screen


def create_video(clear, json_name):
    clear()
    print(json_name)

    with open('./resource/video_configuration.json', 'r') as f:
        configuration = json.load(f)

    with open(f'./json_files/{json_name}.json', 'r') as f:
        data = json.load(f)

    video_clips = []

    # setting the name of the video
    video_name = input('\nEnter the video name: ')

    # get background path
    print(f'\nEnter the quiz template. Bg file should be in the resource')
    template = input('Background name (template01): ') or 'template01'

    question_number = int(input('\nPlase enter the question number (all questions): ') or 0)

    if question_number == 0:
        title = input('\nPlease enter the title for the video: ')

        print(f'\n{Colors.BOLD}Guess break is {configuration["quiz_screen"]["timing"]["guess_break"]}')

        print(f'\n{Colors.WARNING}creating title screens...')

        title_clip = create_title_screen(
            configuration=configuration,
            json_name=json_name,
            template=template,
            title=title
        )

        video_clips.append(title_clip)

        # #  create multiple quiz screens
        print(f'\n{Colors.WARNING}creating multiple quiz screens...')
        for question in data['questions']:
            quiz_clip = create_quiz_screen(
                configuration=configuration,
                question_data=question,
                json_name=json_name,
                template=template
            )
            video_clips.append(quiz_clip)

        # end screen clip
        title_clip = create_title_screen(
            configuration=configuration,
            json_name=json_name,
            template=template,
            title='Thanks for watching!'
        )

        video_clips.append(title_clip)
    else:
        # create single quiz screen
        print('creating single quiz screen')
        quiz_clip = create_quiz_screen(
            configuration=configuration,
            question_data=data['questions'][question_number - 1],
            json_name=json_name,
            template=template,
        )
        video_clips.append(quiz_clip)

    final_video = concatenate_videoclips(video_clips)

    # create background music
    print(f'\n{Colors.ENDC}Please enter the name of the background music with it\'s extension. (0 = no music)')
    bg_music_path = input('Enter: ')
    music = AudioFileClip(f'./bg_music/{bg_music_path}')

    if bg_music_path == 0:
        pass
    else:
        # if music is longer than the video
        if music.duration > (final_video.duration + 5):
            print(f'music dur {music.duration}')
            print(f'video dur {final_video.duration}')
            final_audio = music.set_duration(final_video.duration + 5)
            music = music.volumex(configuration['volume'])
            final_video.audio = CompositeAudioClip([final_video.audio, final_audio])
        # if music is shorter -> loop needed
        else:
            n = math.ceil(final_video.duration) % math.ceil(music.duration-1)
            # gap = final_video.duration - n * (math.ceil(music.duration) - 1)
            # gap_music = music.set_duration(gap)
            print(f'music dur {music.duration}')
            print(f'video dur {final_video.duration}')
            music_loop = concatenate_audioclips((n+1) * [music])  # + [gap_music])
            music_loop = music_loop.volumex(configuration['volume'])
            final_audio = music_loop.set_duration(final_video.duration + 5)
            print(f'music dur {final_audio.duration}')
            print(f'video dur {final_video.duration}')
            final_video.audio = CompositeAudioClip([final_video.audio, final_audio])

    # writing the video file
    final_video.write_videofile(f'./created_videos/{video_name}.mp4', fps=3)

    input('Enter to continue: ')
