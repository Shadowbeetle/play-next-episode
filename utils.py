import os
import pymsgbox
import sys

def get_path_with_folder(dir_list, pattern, exclude, index):
    folder = filter(lambda s: pattern.search(s), sorted(dir_list))[index]
    if folder in exclude:
        return get_path_with_folder(dir_list, pattern, exclude, index + 1)
    return folder

def get_next_file(path, ignored_file_extensions, next_episode):
    file_list = map(os.path.splitext, sorted(os.listdir(path)))
    episode_name_tuples = filter(lambda t: t[1] not in ignored_file_extensions, file_list)
    episodes = map(lambda t: t[0] + t[1], episode_name_tuples)
    episode_file = episodes[next_episode - 1]
    return episode_file

def get_path(path, folder_pattern, exclude, ignored_file_extensions, next_episode, index):
    try:
        folder = get_path_with_folder(os.listdir(path), folder_pattern, exclude, index)
        path_with_folder = path + folder
    except IndexError:
        pymsgbox.alert('Could not find any matching folder in\n\n%s\n\nfor\n\n%s' % (path, folder_pattern.pattern))
        sys.exit(1)

    try:
        next_file = get_next_file(path_with_folder, ignored_file_extensions, next_episode)
    except IndexError:
        exclude.append(folder)
        return get_path(path, folder_pattern, exclude, ignored_file_extensions, 1, index + 1)

    return path_with_folder + '/' + next_file, next_episode