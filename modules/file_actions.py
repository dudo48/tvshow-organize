import os
from . import utility


def move(filepath, new_dir):
    if os.path.samefile(os.path.dirname(filepath), new_dir):
        return
    new_path = os.path.join(new_dir, os.path.basename(filepath))
    os.rename(filepath, new_path)
    return new_path

def rename(filepath, new_name):
    if new_name == utility.get_name(filepath):
        return
    new_name += utility.get_extension(filepath)
    new_path = os.path.join(os.path.dirname(filepath), new_name)
    os.rename(filepath, new_path)
    return new_path
