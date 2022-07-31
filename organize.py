import sys
import os
import argparse
import csv
import pyperclip
from modules import file_actions
from modules import utility
from modules import constants
from modules.constants import *
from services import search
from services import tv
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


# get episodes names either from existing file or using API
def get_episodes_names(show_name, path):
    episodes_names_path = os.path.join(path, constants.EPISODES_NAMES_FILENAME)
    episodes_names = defaultdict(dict)
    
    # read from created file of names if exists else get names using API
    if os.path.isfile(episodes_names_path):
        with open(episodes_names_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                season_number = int(row[0])
                episode_number = int(row[1])
                episode_name = row[2]

                episodes_names[season_number][episode_number] = episode_name
    else:
        # get tv show two times in order to get total count of seasons
        tv_show = search.get_by_name(show_name)
        id = tv_show['id']
        tv_show = tv.get_by_id(id)
        
        for s in tv_show['seasons']:
            season_number = s['season_number']
            season = tv.get_season(id, season_number)
            for ep in season['episodes']:
                episode_number = ep['episode_number']
                episode_name = utility.clean_filename(ep['name'])

                episodes_names[season_number][episode_number] = episode_name
        
        # convert dict to list of lists for easier csv writing
        episodes_names_list = [[s, ep, episodes_names[s][ep]] for s in episodes_names for ep in episodes_names[s]]
        with open(episodes_names_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(episodes_names_list)

    return episodes_names

def standard_rename(path, files):
    show_name = os.path.basename(path)
    episodes_names = get_episodes_names(show_name, path)

    for season_number in sorted(files):
        for episode_number in sorted(files[season_number]):
            for i, filepath in enumerate(files[season_number][episode_number]):
                file_version = '' if i == 0 else i
                format_data = {
                    'show_name': show_name,
                    'season_number': str(season_number).zfill(2),
                    'episode_number': str(episode_number).zfill(2),
                    'episode_name': episodes_names[season_number][episode_number],
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

    if len(sys.argv) > 1:
        args = parser.parse_args()
        path = args.path
    else:
        path = pyperclip.paste()

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
