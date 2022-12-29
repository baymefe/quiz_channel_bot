# main file
import os
import sys
from python_files.colors import Colors
from python_files.get_json import get_json_file
from python_files.download_images import download_images
from python_files.save_audios import save_audios
from python_files.create_video.create_video import create_video
from python_files.create_video.create_short_video import create_short_video
from time import sleep


def main():
    if sys.platform == 'win32':
        def clear():
            return os.system('cls')
    else:
        def clear():
            return os.system('clear')

    while True:
        clear()
        
        print(f'{Colors.HEADER}Welcome to Kahoot Video Maker!\n')

        print(
            f'{Colors.ENDC}'
            '1 Create a json file (and download images with audio)\n'
            '2 Create a video\n'
            '3 Create a short video\n'
            '4 Download image\n'
            '5 Save audio\n'
            '\n99 Get the OS\n'
            '0 Exit'
        )

        ans = input(f'{Colors.WARNING}\nEnter: ')

        match ans:
            case '1':
                # create a json files
                clear()

                print(f'{Colors.HEADER}Please enter the url of the Kahoot quiz\n')
                print(f'{Colors.ENDC}0 Exit\n')

                url = input(f'{Colors.HEADER}URL: ')

                if url == '0':
                    pass
                else:
                    json_name = get_json_file(clear, url)
                    sleep(1)
                    download_images(clear, json_name)
                    sleep(1)
                    save_audios(clear, json_name)

            case '2':
                # create a video
                clear()
                print(f'{Colors.HEADER}Create a video\n')
                print(f'{Colors.ENDC}Please enter the name of the json file')
                print('0 Exit\n')
                json_name = input('File name: ') or 'Nr0001_flagscapitalsofthe2022fifaworldcupfinalscountries'

                if json_name == '0':
                    pass
                else:
                    create_video(clear, json_name)
                pass
            case '3':
                # create a short video
                clear()
                print(f'{Colors.HEADER}Create a short video\n')
                print(f'{Colors.ENDC}Please enter the name of the json file')
                print('0 Exit\n')
                json_name = input('File name: ') or 'Nr0001_flagscapitalsofthe2022fifaworldcupfinalscountries'

                if json_name == '0':
                    pass
                else:
                    create_short_video(clear, json_name)
                pass
            case '4':
                # download images
                clear()
                print(f'{Colors.HEADER}Download images\n')
                print(f'{Colors.ENDC}Please enter the name of the json file\n')
                print('0 Exit\n')

                json_name = input(f'{Colors.WARNING}Enter: ')

                if json_name == '0':
                    pass
                else:
                    download_images(clear, json_name)
            case '5':
                # save audio
                clear()
                print(f'{Colors.HEADER}Save audios\n')
                print(f'{Colors.ENDC}Please enter the name of the json file\n')
                print('0 Exit\n')

                json_name = input(f'{Colors.WARNING}Enter: ')

                if json_name == '0':
                    pass
                else:
                    save_audios(clear, json_name)
            case '99':
                clear()
                input(f'{Colors.OKGREEN}OS is {sys.platform}\n\n{Colors.ENDC}enter to continue:')

            case '0':
                break
            case _:
                input(f'{Colors.FAIL}Please enter a valid value')


if __name__ == '__main__':
    main()
