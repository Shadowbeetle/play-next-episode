#!/usr/bin/env python
import os
import re
import sys
import time
import yaml
import pymsgbox
import subprocess
from tail import tail_f
from utils import get_path, search_for_subtitle_files


def main(should_ask=True, play_previous=False):
    log_reading_timeout = 1

    with open('./setup.yml') as setup_file:
        setup = yaml.load(setup_file)

    try:
        os.remove('./vlc.log')
    except OSError:
        pass

    path = setup["path"] if setup["path"].endswith('/') else setup["path"] + '/'
    name = setup["name"]
    next_episode = setup["next_episode"] if not play_previous else setup["next_episode"] - 2
    audio_language = setup["audio_language"]
    sub_language = setup["sub_language"] if "sub_language" in setup.keys() else False
    exclude = setup["exclude"] if "exclude" in setup.keys() else False

    folder_pattern = re.compile(name.replace(' ', r'[\s_\-\.]?'), flags=re.IGNORECASE)

    subtitle_file_extensions = {'.srt'}
    video_file_extensions = {'.mkv', '.avi', '.mpeg', '.mpg',
                             '.mov', '.flv', '.sfw', '.qt',
                             '.mp4', '.wmv'}

    path, next_file, next_episode = get_path(path, folder_pattern, exclude, video_file_extensions, next_episode, 0)

    if should_ask:
        response = pymsgbox.confirm('Are you sure you want to play the next episode of %s' % name)

        if response == 'Cancel':
            sys.exit(0)

    setup["next_episode"] = next_episode + 1
    setup["exclude"] = exclude

    with open('./setup.yml', 'w') as setup_file:
        yaml.dump(setup, setup_file, default_flow_style=False)

    subtitle_files = search_for_subtitle_files(path, next_file, subtitle_file_extensions)
    sub_file_switch = ''

    if len(subtitle_files) == 1:
        sub_file_switch = '--sub-file=%s' % path + subtitle_files[0]

    audio_language_switch = '' if not audio_language else '--audio-language=%s' % audio_language
    sub_language_switch = '' if not sub_language else '--sub-language=%s' % sub_language
    command = ['vlc', '-f',
               audio_language_switch, sub_language_switch, sub_file_switch,
               "--verbose=2", "--file-logging",
               "--logfile=/home/nazgul/Prog/Home/PlayNextEpisode/vlc.log", "%s" % path + next_file]
    process = subprocess.Popen(command)

    time.sleep(log_reading_timeout)  # wait for the logfile to be created

    pressed_next = 'node: Playlist, skip: 1'
    pressed_prev = 'node: Playlist, skip: -1'
    closed = '-- logger module stopped --'

    with open('./vlc.log') as log:
        for line in tail_f(log):
            if re.search(pressed_next, line):
                process.kill()
                main(False)
            elif re.search(pressed_prev, line):
                process.kill()
                main(False, True)
            elif re.search(closed, line):
                sys.exit(0)


main()
