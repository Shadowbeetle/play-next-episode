#!/usr/bin/env python
import os
import re
import sys
import yaml
import pymsgbox

with open('./setup.yml') as setup_file:
    setup = yaml.load(setup_file)
path = setup["path"] if setup["path"].endswith('/') else setup["path"] + '/'
name = setup["name"]
next_episode = setup["next_episode"]
audio_language = setup["audio_language"]
sub_language = setup["sub_language"] if "sub_language" in setup.keys() else False

folder_pattern = re.compile(name.replace(' ', r'[\s_\-\.]?'), flags=re.IGNORECASE)

ignored_file_extensions = {'.nfo', ''}

try:
    path += filter(lambda s: folder_pattern.search(s), os.listdir(path))[0]
except IndexError:
    pymsgbox.alert('Could not find any matching folder in\n\n%s\n\nfor\n\n%s' % (path, folder_pattern.pattern))
    sys.exit(1)

file_list = map(os.path.splitext, sorted(os.listdir(path)))
episode_name_tuples = filter(lambda t: t[1] not in ignored_file_extensions, file_list)
episodes = map(lambda t: t[0] + t[1], episode_name_tuples)

path += '/' + episodes[next_episode - 1]

response = pymsgbox.confirm('Are you sure you want to play the next episode of %s' % name)

if response == 'Cancel':
    sys.exit(0)

setup["next_episode"] += 1

with open('./setup.yml', 'w') as setup_file:
    yaml.dump(setup, setup_file, default_flow_style=False)

audio_language_switch = '' if not audio_language else '--audio-language=%s' % audio_language
sub_language_switch = '' if not sub_language else '--sub-language=%s' % sub_language
command = 'vlc -f %s %s "%s" &' % (audio_language_switch, sub_language_switch, path)
os.system(command)


sys.exit(0)