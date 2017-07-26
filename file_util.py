import re
from collections import namedtuple

from pymediainfo import MediaInfo

FileInfo = namedtuple('FileInfo', ['container', 'codec', 'size', 'ripping_group'])

def get_file_info(path):
    media_info = MediaInfo.parse(path)
    info_track = media_info.tracks[0]

    container, codec, size = info_track.format, info_track.video_format_list, info_track.file_size

    # best effort to get ripping group name from file name
    match = re.search('\-([a-zA-Z0-9]+)\.[a-zA-Z]+', path)
    ripping_group = match.group(1) if match else None

    return FileInfo(container, codec, size, ripping_group)
