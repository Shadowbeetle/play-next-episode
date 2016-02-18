#!/usr/bin/env python
import os
import re
import sys
import yaml
import pymsgbox
import subprocess
from utils import get_path

with open('./setup.yml') as setup_file:
    setup = yaml.load(setup_file)

path = setup["path"] if setup["path"].endswith('/') else setup["path"] + '/'
name = setup["name"]
next_episode = setup["next_episode"]
audio_language = setup["audio_language"]
sub_language = setup["sub_language"] if "sub_language" in setup.keys() else False
exclude = setup["exclude"] if "exclude" in setup.keys() else False

folder_pattern = re.compile(name.replace(' ', r'[\s_\-\.]?'), flags=re.IGNORECASE)

ignored_file_extensions = {'.nfo', ''}

path, next_episode = get_path(path, folder_pattern, exclude, ignored_file_extensions, next_episode, 0)

response = pymsgbox.confirm('Are you sure you want to play the next episode of %s' % name)

if response == 'Cancel':
    sys.exit(0)

setup["next_episode"] = next_episode + 1
setup["exclude"] = exclude

with open('./setup.yml', 'w') as setup_file:
    yaml.dump(setup, setup_file, default_flow_style=False)

audio_language_switch = '' if not audio_language else '--audio-language=%s' % audio_language
sub_language_switch = '' if not sub_language else '--sub-language=%s' % sub_language
command = ['vlc', '-f', audio_language_switch, sub_language_switch, "--verbose=2", "--file-logging", "--logfile=/home/nazgul/Prog/Home/PlayNextEpisode/vlc.log", "%s" % path]
process = subprocess.Popen(command)

with open('./pid', 'w') as pid_file:
    pid_file.write(str(process.pid))

sys.exit(0)