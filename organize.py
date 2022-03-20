from modules import file_actions
from modules import utility
from modules.constants import *
import os
import argparse
from collections import defaultdict


# returns dict of episodes and dict of subtitles found in a specific path
def create_structure(path):
    episodes = defaultdict(
        lambda: defaultdict(list)
    )

    subtitles = defaultdict(
        lambda: defaultdict(list)
    )

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if utility.is_episode(filename) or utility.is_subtitles(filename):
                season_number = utility.get_season_number(filename)
                episode_number = utility.get_episode_number(filename)
                filepath = os.path.join(dirpath, filename)

                if utility.is_episode(filename):
                    episodes[season_number][episode_number].append(filepath)
                elif utility.is_subtitles(filename):
                    subtitles[season_number][episode_number].append(filepath)

    return episodes, subtitles

def move_episodes(path, files):
    for season_number in sorted(files):
        for episode_number in sorted(files[season_number]):
            for i, filepath in enumerate(files[season_number][episode_number]):
                season_path = os.path.join(
                    path, SEASON_NAME.format(season_number))
                if not os.path.isdir(season_path):
                    os.mkdir(season_path)
                new_path = file_actions.move(filepath, season_path)

                if new_path:
                    files[season_number][episode_number][i] = new_path
                    print(
                        f"Moved '{os.path.basename(filepath)}' to '{os.path.relpath(os.path.dirname(new_path), path)}'")


def move_subtitles(path, files):
    for season_number in sorted(files):
        for episode_number in sorted(files[season_number]):
            for i, filepath in enumerate(files[season_number][episode_number]):

                season_path = os.path.join(
                    path, SEASON_NAME.format(season_number))
                if not os.path.isdir(season_path):
                    os.mkdir(season_path)

                subtitles_path = os.path.join(
                    season_path, SUBTITLE_FOLDER_NAME)
                if not os.path.isdir(subtitles_path):
                    os.mkdir(subtitles_path)

                new_path = file_actions.move(filepath, subtitles_path)
                if new_path:
                    files[season_number][episode_number][i] = new_path
                    print(
                        f"Moved '{os.path.basename(filepath)}' to '{os.path.relpath(os.path.dirname(new_path), path)}'")


def standard_rename(path, files):
    show_name = os.path.basename(path)
    try:
        with open(os.path.join(path, EPISODES_NAMES_FILENAME), encoding='utf-8') as f:
            episodes_names = f.readlines()
        episodes_names = [utility.clean_filename(episode_name)
                          for episode_name in episodes_names]
    except OSError:
        episodes_names = None

    if episodes_names:
        episodes_names_iter = iter(episodes_names)

    for season_number in sorted(files):
        for episode_number in sorted(files[season_number]):

            if episodes_names:
                episode_name = next(episodes_names_iter)
            else:
                episode_name = ''

            for i, filepath in enumerate(files[season_number][episode_number]):
                file_version = '' if i == 0 else i
                format_data = {
                    'show_name': show_name,
                    'season_number': str(season_number).zfill(2),
                    'episode_number': str(episode_number).zfill(2),
                    'episode_name': episode_name,
                    'file_version': file_version
                }

                filename = [str.format_map(part, format_data) for part in EPISODE_STANDARD_NAME]
                filename = [s for s in filename if s]
                filename = STANDARD_SEPARATOR.join(filename)

                old_name = os.path.basename(filepath)
                new_path = file_actions.rename(filepath, filename)
                if new_path:
                    files[season_number][episode_number][i] = new_path
                    print(f"Renamed '{old_name}' to '{os.path.basename(new_path)}'")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()

    path = args.path
    if not os.path.isdir(path):
        print("Invalid path")
        return

    episodes, subtitles = create_structure(path)
    standard_rename(path, episodes)
    standard_rename(path, subtitles)

    move_episodes(path, episodes)
    move_subtitles(path, subtitles)

    print("Done")


if __name__ == '__main__':
    main()
