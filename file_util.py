import re
import os
import shutil
from collections import namedtuple

from pymediainfo import MediaInfo

from dirs import TEMP_PATH, MOVIE_PATH

FileInfo = namedtuple('FileInfo', ['container', 'codec', 'size'])

def get_temp_files():
    return os.listdir(TEMP_PATH)

def get_file_info(path):
    media_info = MediaInfo.parse(path)
    info_track = media_info.tracks[0]

    container, codec, size = info_track.format, info_track.video_format_list, info_track.file_size

    return FileInfo(container, codec, size)

def get_file_info_temp(file_name):
    return get_file_info(os.path.join(TEMP_PATH, file_name))

def get_ripping_group(path):
    # best effort to get ripping group name from file name
    match = re.search('\-([a-zA-Z0-9]+)\.[a-zA-Z]+', path)
    ripping_group = match.group(1) if match else None

    return ripping_group

def check_tmp_filename(file_name):
    return os.path.isfile(os.path.join(TEMP_PATH, file_name))

def move_temp_file_to_collection(tmp_file, new_name):
    shutil.move(os.path.join(TEMP_PATH, tmp_file), os.path.join(MOVIE_PATH, new_name))
