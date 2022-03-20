import os

from numpy import mat
from . import constants
import re
from . import patterns


# checks if the given filename is an episode
def is_episode(basename):
    filename = os.path.splitext(basename)[0].lower()
    extension = os.path.splitext(basename)[1].lower()[1:]
    return extension in constants.VIDEOS_EXTENSIONS and re.search(patterns.EPISODE_NUMBER_PATTERN, filename, re.I)


# checks if the given filename is a subtitle
def is_subtitles(basename):
    filename = os.path.splitext(basename)[0].lower()
    extension = os.path.splitext(basename)[1].lower()[1:]
    return extension in constants.SUBTITLES_EXTENSIONS and re.search(patterns.EPISODE_NUMBER_PATTERN, filename, re.I)


# returns season number of the given file name
def get_season_number(filename):
    matches = re.search(patterns.SEASON_NUMBER_PATTERN, filename, re.I)
    return int(next((m for m in matches.groups() if m is not None), 0))


# returns season number of the given file name
def get_episode_number(filename):
    matches = re.search(patterns.EPISODE_NUMBER_PATTERN, filename, re.I)
    return int(next(m for m in matches.groups() if m is not None))


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
