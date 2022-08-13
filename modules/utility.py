import os
from . import constants
import re
from . import patterns


# returns season number of the given file name
def get_season_number(filename):
    for p in patterns.SEASON_NUMBER_PATTERNS:
        match = re.search(p, filename, re.I)
        if match:
            return int(match.group(1))
    return None


# returns episode number of the given file name
def get_episode_number(filename):
    for p in patterns.EPISODE_NUMBER_PATTERNS:
        match = re.search(p, filename, re.I)
        if match:
            return int(match.group(1))
    return None


# checks if the given filename is an episode
def is_episode(basename):
    filename = os.path.splitext(basename)[0].lower()
    extension = os.path.splitext(basename)[1].lower()[1:]
    return extension in constants.VIDEOS_EXTENSIONS and get_episode_number(filename)


# checks if the given filename is a subtitle
def is_subtitles(basename):
    filename = os.path.splitext(basename)[0].lower()
    extension = os.path.splitext(basename)[1].lower()[1:]
    return extension in constants.SUBTITLES_EXTENSIONS and get_episode_number(filename)


# returns name without extension
def get_name(path):
    return os.path.splitext(os.path.basename(path))[0]


def get_extension(path):
    return os.path.splitext(os.path.basename(path))[1]


# remove trailing white space and illegal characters
def clean_filename(filename):
    filename = re.sub('[/\\\\:?*"<>|]', '', filename)
    filename = filename.strip()

    return filename
