import os
import tkMessageBox
import sys


def get_path_with_folder(dir_list, pattern, exclude, index):
    folder = filter(lambda s: pattern.search(s), sorted(dir_list))[index]
    if folder in exclude:
        return get_path_with_folder(dir_list, pattern, exclude, index + 1)
    return folder


def get_suitable_files(file_list, accepted_file_extensions):
    file_list = map(os.path.splitext, file_list)
    filename_tuples = filter(lambda t: t[1] in accepted_file_extensions, file_list)
    filenames = map(lambda t: t[0] + t[1], filename_tuples)
    return filenames


def get_next_file(path, accepted_file_extensions, next_episode):
    episodes = get_suitable_files(sorted(os.listdir(path)), accepted_file_extensions)
    episode_file = episodes[next_episode - 1]
    return episode_file


def get_path(path, folder_pattern, exclude, accepted_file_extensions, next_episode, index):
    try:
        folder = get_path_with_folder(os.listdir(path), folder_pattern, exclude, index)
        path_with_folder = path + folder
    except IndexError:
        tkMessageBox.showerror(message='Could not find any matching folder in\n\n%s\n\nfor\n\n%s' % (path, folder_pattern.pattern))
        sys.exit(1)

    try:
        next_file = get_next_file(path_with_folder, accepted_file_extensions, next_episode)
    except (IndexError, OSError):
        exclude.append(folder)
        return get_path(path, folder_pattern, exclude, accepted_file_extensions, 1, index + 1)

    return path_with_folder + '/', next_file, next_episode


def search_for_subtitle_files(path, video_name, accepted_file_extensions):
    video_name = os.path.splitext(video_name)
    file_list = get_suitable_files(os.listdir(path), accepted_file_extensions)
    filtered_file_list = filter(lambda s: os.path.splitext(s) != video_name, file_list)
    return sorted(filtered_file_list)
